"""
Real OSINT Modules for Phone Number Analysis

This module uses actual APIs for legitimate phone number verification and fraud detection.
"""

import requests
import os
from typing import Dict, List
from datetime import datetime

# Get API keys from environment variables
NUMVERIFY_API_KEY = os.getenv('NUMVERIFY_API_KEY', '')
IPQUALITYSCORE_API_KEY = os.getenv('IPQUALITYSCORE_API_KEY', '')
ABSTRACT_API_KEY = os.getenv('ABSTRACT_API_KEY', '')


class BaseScanner:
    """Base class for all OSINT scanners"""
    
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.results = {}
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def _make_request(self, url, method='GET', headers=None, data=None, params=None):
        """Make HTTP request with error handling"""
        try:
            default_headers = {'User-Agent': self.user_agent}
            if headers:
                default_headers.update(headers)
                
            if method == 'GET':
                response = requests.get(url, headers=default_headers, params=params, timeout=15)
            else:
                response = requests.post(url, headers=default_headers, json=data, timeout=15)
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None


class NumverifyValidator(BaseScanner):
    """
    Use Numverify API for phone validation and carrier lookup
    API Docs: https://numverify.com/documentation
    Free tier: 100 requests/month
    """
    
    def validate(self) -> Dict:
        """Validate phone number and get carrier info"""
        if not NUMVERIFY_API_KEY:
            return {
                'error': 'NUMVERIFY_API_KEY not configured',
                'valid': False
            }
        
        url = 'http://apilayer.net/api/validate'
        params = {
            'access_key': NUMVERIFY_API_KEY,
            'number': self.phone_number,
            'country_code': '',
            'format': 1
        }
        
        data = self._make_request(url, params=params)
        
        if data and data.get('valid'):
            return {
                'valid': True,
                'number': data.get('international_format', ''),
                'local_format': data.get('local_format', ''),
                'country_code': data.get('country_code', ''),
                'country_name': data.get('country_name', ''),
                'location': data.get('location', ''),
                'carrier': data.get('carrier', 'Unknown'),
                'line_type': data.get('line_type', 'Unknown')
            }
        
        return {
            'valid': False,
            'error': data.get('error', {}).get('info', 'Invalid number') if data else 'API error'
        }


class IPQualityScoreChecker(BaseScanner):
    """
    Use IPQualityScore API for fraud detection
    API Docs: https://www.ipqualityscore.com/documentation/phone-number-validation-api/overview
    Free tier: 5,000 requests/month
    """
    
    def check_fraud(self) -> Dict:
        """Check phone number for fraud indicators"""
        if not IPQUALITYSCORE_API_KEY:
            return {
                'error': 'IPQUALITYSCORE_API_KEY not configured',
                'fraud_score': 0
            }
        
        # Remove + and spaces from phone number
        clean_number = self.phone_number.replace('+', '').replace(' ', '')
        
        url = f'https://ipqualityscore.com/api/json/phone/{IPQUALITYSCORE_API_KEY}/{clean_number}'
        params = {
            'strictness': 1,  # 0-2, higher = more strict
            'country[]': 'US'  # Can specify multiple countries
        }
        
        data = self._make_request(url, params=params)
        
        if data and data.get('success'):
            return {
                'fraud_score': data.get('fraud_score', 0),  # 0-100
                'recent_abuse': data.get('recent_abuse', False),
                'VOIP': data.get('VOIP', False),
                'prepaid': data.get('prepaid', False),
                'risky': data.get('risky', False),
                'active': data.get('active', False),
                'carrier': data.get('carrier', 'Unknown'),
                'line_type': data.get('line_type', 'Unknown'),
                'country': data.get('country', ''),
                'city': data.get('city', ''),
                'region': data.get('region', ''),
                'spam_score': data.get('spam_score', 0),
                'do_not_call': data.get('do_not_call', False)
            }
        
        return {
            'error': data.get('message', 'API error') if data else 'Request failed',
            'fraud_score': 0
        }


class AbstractPhoneValidator(BaseScanner):
    """
    Use Abstract API for phone validation
    API Docs: https://www.abstractapi.com/phone-validation-api
    Free tier: 250 requests/month
    """
    
    def validate(self) -> Dict:
        """Validate and get phone info"""
        if not ABSTRACT_API_KEY:
            return {
                'error': 'ABSTRACT_API_KEY not configured',
                'valid': False
            }
        
        url = 'https://phonevalidation.abstractapi.com/v1/'
        params = {
            'api_key': ABSTRACT_API_KEY,
            'phone': self.phone_number
        }
        
        data = self._make_request(url, params=params)
        
        if data and data.get('valid'):
            return {
                'valid': True,
                'format': {
                    'international': data.get('format', {}).get('international', ''),
                    'local': data.get('format', {}).get('local', '')
                },
                'country': {
                    'code': data.get('country', {}).get('code', ''),
                    'name': data.get('country', {}).get('name', ''),
                    'prefix': data.get('country', {}).get('prefix', '')
                },
                'type': data.get('type', 'Unknown'),
                'carrier': data.get('carrier', 'Unknown')
            }
        
        return {
            'valid': False,
            'error': 'Invalid phone number'
        }


class SpamDatabaseChecker(BaseScanner):
    """
    Check phone number against spam databases
    Uses free/public APIs and databases
    """
    
    def check(self) -> Dict:
        """Check against spam databases"""
        results = {
            'total_reports': 0,
            'details': [],
            'sources': [],
            'categories': []
        }
        
        # Use IPQualityScore spam data if available
        if IPQUALITYSCORE_API_KEY:
            ipqs = IPQualityScoreChecker(self.phone_number)
            fraud_data = ipqs.check_fraud()
            
            if not fraud_data.get('error'):
                spam_score = fraud_data.get('spam_score', 0)
                if spam_score > 0:
                    results['total_reports'] = int(spam_score / 10)  # Convert score to report count
                    results['sources'].append('IPQualityScore')
                    results['details'].append({
                        'source': 'IPQualityScore',
                        'report_count': results['total_reports'],
                        'categories': ['Spam' if spam_score > 50 else 'Potential Spam'],
                        'spam_score': spam_score,
                        'last_reported': datetime.now().strftime('%Y-%m-%d')
                    })
                    
                    if fraud_data.get('recent_abuse'):
                        results['categories'].append('Recent Abuse')
                    if fraud_data.get('VOIP'):
                        results['categories'].append('VOIP')
        
        # You can add more APIs here:
        # - TrueCaller API (paid)
        # - Twilio Lookup API
        # - Custom database queries
        
        results['categories'] = list(set(results['categories']))
        return results


class SocialMediaScanner(BaseScanner):
    """
    Scan social media platforms for phone number presence
    Note: Most social media APIs require OAuth and don't allow phone number searches
    This provides framework for when you have proper API access
    """
    
    def scan(self) -> Dict:
        """
        Scan social media platforms
        
        IMPORTANT: Most platforms don't allow automated phone searches
        This requires:
        - Official API access
        - User consent
        - OAuth tokens
        """
        results = {
            'platforms_checked': [],
            'accounts_found': [],
            'anomaly_detected': False,
            'anomaly_description': None,
            'warning': 'Social media scanning requires official API access and user consent'
        }
        
        # TODO: Implement when you have:
        # - Facebook Graph API access
        # - Twitter API v2 access
        # - LinkedIn API access
        # All require OAuth and app approval
        
        return results


class FraudForumScanner(BaseScanner):
    """Scan public fraud forums and databases"""
    
    def scan(self) -> Dict:
        """
        Search for phone number in public fraud reports
        """
        results = {
            'mentions_count': 0,
            'mentions': [],
            'risk_level': 'LOW',
            'sources_checked': []
        }
        
        # Use IPQualityScore data if available
        if IPQUALITYSCORE_API_KEY:
            ipqs = IPQualityScoreChecker(self.phone_number)
            fraud_data = ipqs.check_fraud()
            
            if not fraud_data.get('error'):
                if fraud_data.get('recent_abuse') or fraud_data.get('risky'):
                    results['mentions_count'] = 1
                    results['mentions'].append({
                        'source': 'IPQualityScore Fraud Database',
                        'context': 'Phone number flagged for suspicious activity',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'severity': 'HIGH' if fraud_data.get('recent_abuse') else 'MEDIUM',
                        'fraud_score': fraud_data.get('fraud_score', 0)
                    })
                    results['risk_level'] = 'HIGH' if fraud_data.get('fraud_score', 0) > 75 else 'MEDIUM'
        
        results['sources_checked'].append('IPQualityScore')
        return results


# Telegram and WhatsApp scanning require official APIs and proper authorization
# These are placeholders showing what data structure to expect

class TelegramScanner(BaseScanner):
    """
    Telegram scanning requires Telethon library and API credentials
    Get API credentials: https://my.telegram.org/apps
    """
    
    def scan(self) -> Dict:
        return {
            'has_telegram_account': False,
            'public_username': None,
            'warning': 'Requires Telegram API credentials and user consent',
            'setup_instructions': 'Install telethon: pip install telethon, Get API ID and Hash from https://my.telegram.org/apps'
        }


class WhatsAppChecker(BaseScanner):
    """
    WhatsApp Business API required for legitimate checking
    Signup: https://developers.facebook.com/docs/whatsapp
    """
    
    def check(self) -> Dict:
        return {
            'has_whatsapp': False,
            'business_account': False,
            'warning': 'Requires WhatsApp Business API access',
            'setup_instructions': 'Apply for WhatsApp Business API at https://developers.facebook.com/docs/whatsapp'
        }
