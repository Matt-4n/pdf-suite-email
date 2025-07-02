# Use Node.js 18 with Python support
FROM node:18-bullseye

# Install Python and system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ghostscript \
    imagemagick \
    qpdf \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy Python requirements and install Python dependencies
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy Node.js package files
COPY package*.json ./

# Install Node.js dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p uploads outputs merger-uploads merger-outputs logs signatures manifests && \
    chmod 755 uploads outputs merger-uploads merger-outputs logs signatures manifests

# Create a default signature placeholder if none exists
RUN mkdir -p signatures && \
    echo "Placeholder for signature file" > signatures/README.txt

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["node", "server.js"]