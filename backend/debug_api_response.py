"""Debug script to check API responses for Indian number"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.services.osint_modules import IPQualityScoreChecker, NumverifyValidator
import json

app = create_app()

with app.app_context():
    test_number = "+919967983221"
    
    print(f"Testing API responses for {test_number}")
    print("=" * 80)
    
    # IPQualityScore
    print("\n1️⃣ IPQualityScore Response:")
    print("-" * 80)
    ipqs = IPQualityScoreChecker(test_number)
    ipqs_data = ipqs.check_fraud()
    print(json.dumps(ipqs_data, indent=2))
    
    # Numverify
    print("\n2️⃣ Numverify Response:")
    print("-" * 80)
    numverify = NumverifyValidator(test_number)
    numverify_data = numverify.validate()
    print(json.dumps(numverify_data, indent=2))
    
    print("\n" + "=" * 80)
    print("\n📊 Analysis:")
    print(f"  Active (IPQS): {ipqs_data.get('active')}")
    print(f"  Valid (Numverify): {numverify_data.get('valid')}")
    print(f"  VOIP (IPQS): {ipqs_data.get('VOIP')}")
    print(f"  Prepaid (IPQS): {ipqs_data.get('prepaid')}")
    print(f"  Line Type (Numverify): {numverify_data.get('line_type')}")
    print(f"  Carrier (IPQS): {ipqs_data.get('carrier')}")
    print(f"  Carrier (Numverify): {numverify_data.get('carrier')}")
