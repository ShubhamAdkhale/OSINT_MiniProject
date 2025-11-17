"""
Test script to verify API configuration
Run this to check if your API keys are working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.osint_modules_real import (
    NumverifyValidator,
    IPQualityScoreChecker,
    AbstractPhoneValidator,
    SpamDatabaseChecker
)

def test_ipqualityscore():
    """Test IPQualityScore API"""
    print("\n" + "="*50)
    print("Testing IPQualityScore API...")
    print("="*50)
    
    api_key = os.getenv('IPQUALITYSCORE_API_KEY')
    if not api_key:
        print("❌ IPQUALITYSCORE_API_KEY not found in .env file")
        print("   Sign up at: https://www.ipqualityscore.com/create-account")
        return False
    
    checker = IPQualityScoreChecker("+14158586273")  # Test with Google's number
    result = checker.check_fraud()
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
        return False
    
    print("✅ IPQualityScore API is working!")
    print(f"   Fraud Score: {result.get('fraud_score', 0)}/100")
    print(f"   Carrier: {result.get('carrier', 'Unknown')}")
    print(f"   Line Type: {result.get('line_type', 'Unknown')}")
    print(f"   Country: {result.get('country', 'Unknown')}")
    print(f"   Active: {result.get('active', False)}")
    return True

def test_numverify():
    """Test Numverify API"""
    print("\n" + "="*50)
    print("Testing Numverify API...")
    print("="*50)
    
    api_key = os.getenv('NUMVERIFY_API_KEY')
    if not api_key:
        print("⚠️  NUMVERIFY_API_KEY not found in .env file")
        print("   Sign up at: https://numverify.com/product")
        print("   (Optional - IPQualityScore can replace this)")
        return False
    
    validator = NumverifyValidator("+14158586273")
    result = validator.validate()
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
        return False
    
    print("✅ Numverify API is working!")
    print(f"   Number: {result.get('number', '')}")
    print(f"   Carrier: {result.get('carrier', 'Unknown')}")
    print(f"   Country: {result.get('country_name', 'Unknown')}")
    print(f"   Line Type: {result.get('line_type', 'Unknown')}")
    return True

def test_abstract():
    """Test Abstract API"""
    print("\n" + "="*50)
    print("Testing Abstract API...")
    print("="*50)
    
    api_key = os.getenv('ABSTRACT_API_KEY')
    if not api_key:
        print("⚠️  ABSTRACT_API_KEY not found in .env file")
        print("   Sign up at: https://www.abstractapi.com/phone-validation-api")
        print("   (Optional - IPQualityScore can replace this)")
        return False
    
    validator = AbstractPhoneValidator("+14158586273")
    result = validator.validate()
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
        return False
    
    print("✅ Abstract API is working!")
    print(f"   Number: {result.get('format', {}).get('international', '')}")
    print(f"   Carrier: {result.get('carrier', 'Unknown')}")
    print(f"   Country: {result.get('country', {}).get('name', 'Unknown')}")
    print(f"   Type: {result.get('type', 'Unknown')}")
    return True

def test_spam_checker():
    """Test spam database integration"""
    print("\n" + "="*50)
    print("Testing Spam Database Checker...")
    print("="*50)
    
    checker = SpamDatabaseChecker("+14158586273")
    result = checker.check()
    
    print("✅ Spam checker is working!")
    print(f"   Total Reports: {result.get('total_reports', 0)}")
    print(f"   Sources: {', '.join(result.get('sources', ['None']))}")
    print(f"   Categories: {', '.join(result.get('categories', ['None']))}")
    return True

def main():
    """Run all API tests"""
    print("\n" + "="*60)
    print("🔍 OSINT API Configuration Test")
    print("="*60)
    print("\nThis will test your API keys and verify they're working.\n")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found in backend directory")
        print("   Please create a .env file with your API keys")
        print("   See API_SETUP_GUIDE.md for instructions")
        return
    
    results = {
        'IPQualityScore': test_ipqualityscore(),
        'Numverify': test_numverify(),
        'Abstract': test_abstract(),
        'SpamChecker': test_spam_checker()
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    working = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}: {'Working' if status else 'Not Configured/Failed'}")
    
    print("\n" + "="*60)
    
    if results['IPQualityScore']:
        print("✅ Core functionality is working!")
        print("   IPQualityScore provides fraud detection and spam checking.")
        print("\n   Your OSINT system is ready to use with real data!")
    else:
        print("⚠️  IPQualityScore is required for core functionality.")
        print("\n   Next steps:")
        print("   1. Sign up at: https://www.ipqualityscore.com/create-account")
        print("   2. Get your API key from the dashboard")
        print("   3. Add to backend/.env: IPQUALITYSCORE_API_KEY=your_key_here")
        print("   4. Run this test again")
    
    print("\n   See API_SETUP_GUIDE.md for detailed instructions")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
