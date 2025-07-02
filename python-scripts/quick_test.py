#!/usr/bin/env python3
"""
Quick test for PDF merger fixes
"""

def test_reference_matching():
    """Test the new reference matching logic"""
    print("🧪 Testing Reference Matching Logic...")
    
    # Mock EDI manifest (like your real data)
    manifest = {
        '000/527/962/A': 'Louis Roux',
        '000/536/387/A': 'Kristiaan Alfons L. Willems',
        '000/531/023': 'Bruce De Clifford Mastoroudes',
        '000/534/927': 'Simone Ganasen'
    }
    
    # Test references found in documents
    test_refs = ['000/527/962', '000/536/387', '000/531/023', '000/999/999']
    
    for ref_normalized in test_refs:
        print(f"\n📄 Testing reference: {ref_normalized}")
        
        # NEW LOGIC: Match on first 11 characters
        ref_base = ref_normalized[:11]  # Get first 11 characters
        
        # Find matching EDI reference
        matched_ref = None
        for edi_ref in manifest.keys():
            if edi_ref[:11] == ref_base:
                matched_ref = edi_ref
                break
        
        if matched_ref:
            client_name = manifest[matched_ref]
            print(f"   ✅ Found {ref_normalized} -> {matched_ref} - {client_name}")
        else:
            print(f"   ❌ No match found for {ref_normalized}")

def test_hbl_detection():
    """Test HBL file detection"""
    print("\n🧪 Testing HBL File Detection...")
    
    # Test filenames from your uploads
    test_files = [
        '1750864020848-731834473-000-527-962-A_HBL.pdf',
        '1750864020869-31795347-000-531-023_HBL.pdf',
        '1750951225240-531489799-Advice of Arrival ICR1032487.pdf',
        '1750942802004-956201118-000-531-318_Document.pdf',
        'Bill_of_Lading_1.pdf',
        'some_other_file.pdf'
    ]
    
    for filename in test_files:
        filename_lower = filename.lower()
        
        # Test the detection logic
        if ('advice' in filename_lower and 'arrival' in filename_lower):
            category = "📋 Advice of Arrival"
        elif (('bill' in filename_lower and 'lading' in filename_lower) or 
              'bills_of_lading' in filename_lower or 
              filename_lower.startswith('bill_of_lading') or
              filename_lower.startswith('bill') or
              '_hbl.pdf' in filename_lower or
              filename_lower.endswith('_hbl.pdf') or
              'hbl' in filename_lower):
            category = "🚢 Bill of Lading"
        else:
            category = "👥 Customer Document"
            
        print(f"   {category}: {filename}")

def test_tax_alerts_structure():
    """Test the tax alerts data structure for JSON output"""
    print("\n🧪 Testing Tax Alerts JSON Structure...")
    
    # Mock tax alerts data (like what your system generates)
    mock_tax_alerts = [
        {
            'client_name': 'Leren Smart',
            'client_ref': '000/535/582',
            'alerts': [
                {'keyword': 'TOOLS', 'page': 14, 'context': 'Various tools and equipment'},
                {'keyword': 'NEW', 'page': 21, 'context': 'New imported goods'}
            ]
        },
        {
            'client_name': 'Jaroslava Momberg', 
            'client_ref': '000/537/706',
            'alerts': [
                {'keyword': 'TOOLS', 'page': 17, 'context': 'Workshop tools'},
                {'keyword': 'ALCOHOL', 'page': 25, 'context': 'Alcoholic beverages'}
            ]
        }
    ]
    
    # Test JSON serialization (what gets sent to web interface)
    import json
    
    mock_result = {
        'success': True,
        'message': 'Processing completed successfully',
        'output_folder': '/path/to/output',
        'stats': {'merged_clients': 17},
        'tax_alerts': mock_tax_alerts  # This is what we added
    }
    
    try:
        json_output = json.dumps(mock_result, indent=2)
        print("   ✅ JSON serialization successful")
        print("   📊 Sample tax alerts structure:")
        
        for alert in mock_tax_alerts:
            print(f"      🚨 {alert['client_name']} ({alert['client_ref']})")
            for item in alert['alerts']:
                print(f"         • {item['keyword']} found on page {item['page']}")
        
        # Test what the web interface would receive
        parsed_result = json.loads(json_output)
        if 'tax_alerts' in parsed_result and len(parsed_result['tax_alerts']) > 0:
            print(f"   ✅ Web interface would receive {len(parsed_result['tax_alerts'])} tax alerts")
        else:
            print("   ❌ No tax alerts in JSON output")
            
    except Exception as e:
        print(f"   ❌ JSON serialization failed: {e}")

if __name__ == "__main__":
    test_reference_matching()
    test_hbl_detection()
    test_tax_alerts_structure()
    print("\n✅ All tests complete!")