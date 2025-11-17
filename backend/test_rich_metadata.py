"""
Quick test script to verify rich metadata collection
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.services.phone_analyzer import PhoneAnalyzer
import json

app = create_app()

with app.app_context():
    # Test with a known phone number
    test_number = "+14158586273"  # Google voice number
    
    analyzer = PhoneAnalyzer(test_number)
    
    print(f"Analyzing {test_number}...")
    print("=" * 60)
    
    result = analyzer.analyze()
    
    # Print rich metadata
    if 'rich_metadata' in result:
        print("\n✅ RICH METADATA COLLECTED:")
        print(json.dumps(result['rich_metadata'], indent=2))
    else:
        print("\n❌ No rich metadata found in result")
    
    print("\n" + "=" * 60)
    print(f"Risk Score: {result.get('risk_score')}/100")
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"Carrier: {result.get('carrier')}")
    print(f"Line Type: {result.get('line_type')}")
    print(f"Country: {result.get('country_code')}")
