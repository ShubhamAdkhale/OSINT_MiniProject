import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import time
from app.services.osint_modules import (
    NumverifyValidator,
    IPQualityScoreChecker,
    AbstractPhoneValidator,
    SpamDatabaseChecker,
    FraudForumScanner,
    SocialMediaScanner,
    TelegramScanner,
    WhatsAppChecker
)
from app.services.risk_scorer import RiskScorer

class PhoneAnalyzer:
    """Main phone number analysis orchestrator"""
    
    def __init__(self, phone_number, deep_scan=False):
        self.phone_number = phone_number
        self.deep_scan = deep_scan
        self.results = {
            'phone_number': phone_number,
            'data_sources_used': [],
            'risk_factors': []
        }
        
    def analyze(self):
        """Perform complete analysis"""
        try:
            # Step 1: Basic phone validation and info
            self._get_basic_info()
            
            # Step 2: Enhanced metadata from APIs
            self._get_rich_metadata()
            
            # Step 3: Social media presence check
            self._check_social_media()
            
            # Step 4: Spam database check
            self._check_spam_databases()
            
            # Step 5: Fraud forum scan
            self._check_fraud_forums()
            
            # Step 6: Messaging app presence
            self._check_messaging_apps()
            
            # Step 7: Calculate risk score
            self._calculate_risk()
            
            return self.results
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _get_basic_info(self):
        """Extract basic phone number information"""
        try:
            parsed = phonenumbers.parse(self.phone_number, None)
            
            self.results['country_code'] = f"+{parsed.country_code}"
            self.results['carrier'] = carrier.name_for_number(parsed, "en") or "Unknown"
            self.results['line_type'] = phonenumbers.number_type(parsed)
            self.results['location'] = geocoder.description_for_number(parsed, "en") or "Unknown"
            self.results['timezones'] = timezone.time_zones_for_number(parsed)
            
            self.results['data_sources_used'].append('phonenumbers_library')
            
        except Exception as e:
            self.results['basic_info_error'] = str(e)
    
    def _get_rich_metadata(self):
        """Get enhanced metadata from IPQualityScore and Numverify"""
        try:
            # Get IPQualityScore data
            ipqs_checker = IPQualityScoreChecker(self.phone_number)
            ipqs_data = ipqs_checker.check_fraud()
            
            # Get Numverify data
            numverify = NumverifyValidator(self.phone_number)
            numverify_data = numverify.validate()
            
            # Determine prepaid status with better logic
            # IPQualityScore free tier has limited prepaid detection, especially for non-US numbers
            is_prepaid = ipqs_data.get('prepaid', None)
            line_type_value = ipqs_data.get('line_type', '').lower()
            
            # If prepaid status is unknown and line type suggests mobile, assume prepaid for certain countries
            if is_prepaid is None or (is_prepaid is False and ipqs_data.get('country') in ['IN', 'PH', 'ID', 'BD']):
                # In India and similar markets, most mobile numbers are prepaid
                if 'mobile' in line_type_value or 'wireless' in line_type_value:
                    is_prepaid = None  # Unknown, but likely prepaid in these markets
            
            # Compile rich metadata
            rich_metadata = {
                'carrier_details': {
                    'current_carrier': ipqs_data.get('carrier') or numverify_data.get('carrier', 'Unknown'),
                    'original_carrier': numverify_data.get('carrier', 'Unknown'),
                    'porting_detected': False,  # Will be true if carriers don't match
                    'line_type': ipqs_data.get('line_type') or numverify_data.get('line_type', 'Unknown'),
                    'is_voip': ipqs_data.get('VOIP', False),
                    'is_prepaid': is_prepaid,
                },
                'geographic_data': {
                    'country': ipqs_data.get('country', ''),
                    'country_name': numverify_data.get('country_name', ''),
                    'city': ipqs_data.get('city') if ipqs_data.get('city') != 'N/A' else numverify_data.get('location', 'Unknown'),
                    'region': ipqs_data.get('region', 'Unknown'),
                    'location_formatted': numverify_data.get('location', ''),
                    'timezone': self.results.get('timezones', [])[0] if self.results.get('timezones') else 'Unknown',
                    'all_timezones': self.results.get('timezones', []),
                },
                'number_status': {
                    'active': ipqs_data.get('active', True),  # Default to True if unknown
                    'valid': numverify_data.get('valid', False),
                    'risky': ipqs_data.get('risky', False),
                    'do_not_call': ipqs_data.get('do_not_call', False),
                },
                'reputation_indicators': {
                    'fraud_score': ipqs_data.get('fraud_score', 0),
                    'spam_score': ipqs_data.get('spam_score', 0),
                    'recent_abuse': ipqs_data.get('recent_abuse', False),
                    'leak_detected': False,  # Would be from data breach checks
                }
            }
            
            # Detect porting (if carriers don't match)
            if (rich_metadata['carrier_details']['current_carrier'] != 'Unknown' and 
                rich_metadata['carrier_details']['original_carrier'] != 'Unknown' and
                rich_metadata['carrier_details']['current_carrier'] != rich_metadata['carrier_details']['original_carrier']):
                rich_metadata['carrier_details']['porting_detected'] = True
                rich_metadata['carrier_details']['porting_history'] = [
                    {'carrier': rich_metadata['carrier_details']['original_carrier'], 'status': 'Original'},
                    {'carrier': rich_metadata['carrier_details']['current_carrier'], 'status': 'Current'}
                ]
            
            # Estimate number age based on carrier type and activity
            if ipqs_data.get('active'):
                if ipqs_data.get('VOIP'):
                    rich_metadata['estimated_age'] = 'Recent (VOIP numbers are typically newer)'
                elif ipqs_data.get('prepaid'):
                    rich_metadata['estimated_age'] = 'Variable (Prepaid numbers can be recycled)'
                else:
                    rich_metadata['estimated_age'] = 'Established (Active traditional line)'
            else:
                rich_metadata['estimated_age'] = 'Unknown or Inactive'
            
            self.results['rich_metadata'] = rich_metadata
            self.results['data_sources_used'].extend(['IPQualityScore', 'Numverify'])
            
            # Add risk factors based on metadata
            if rich_metadata['carrier_details']['is_voip']:
                self.results['risk_factors'].append({
                    'category': 'carrier',
                    'factor_type': 'voip_number',
                    'severity': 'MEDIUM',
                    'weight': 0.15,
                    'description': 'VOIP numbers are commonly used in fraud schemes',
                    'evidence': {'is_voip': True},
                    'source': 'Carrier Analysis'
                })
            
            if rich_metadata['carrier_details']['porting_detected']:
                self.results['risk_factors'].append({
                    'category': 'carrier',
                    'factor_type': 'porting_detected',
                    'severity': 'LOW',
                    'weight': 0.10,
                    'description': 'Number has been ported between carriers',
                    'evidence': rich_metadata['carrier_details'].get('porting_history', []),
                    'source': 'Carrier Analysis'
                })
            
            if rich_metadata['number_status']['do_not_call']:
                self.results['risk_factors'].append({
                    'category': 'compliance',
                    'factor_type': 'do_not_call_registry',
                    'severity': 'LOW',
                    'weight': 0.05,
                    'description': 'Number is on Do Not Call registry',
                    'evidence': {'do_not_call': True},
                    'source': 'Compliance Check'
                })
                
        except Exception as e:
            self.results['rich_metadata_error'] = str(e)
    
    def _check_social_media(self):
        """Check social media presence"""
        try:
            scanner = SocialMediaScanner(self.phone_number)
            social_results = scanner.scan()
            
            self.results['social_media_presence'] = social_results
            self.results['data_sources_used'].extend(['social_media_scan'])
            
            # Add risk factors if anomalies found
            if social_results.get('anomaly_detected'):
                self.results['risk_factors'].append({
                    'category': 'social_media',
                    'factor_type': 'suspicious_activity',
                    'severity': social_results.get('severity', 'MEDIUM'),
                    'weight': 0.30,
                    'description': social_results.get('anomaly_description'),
                    'evidence': social_results,
                    'source': 'Social Media Scan'
                })
                
        except Exception as e:
            self.results['social_media_error'] = str(e)
    
    def _check_spam_databases(self):
        """Check spam/scam databases"""
        try:
            checker = SpamDatabaseChecker(self.phone_number)
            spam_results = checker.check()
            
            self.results['spam_reports_count'] = spam_results.get('total_reports', 0)
            self.results['spam_details'] = spam_results.get('details', [])
            self.results['data_sources_used'].extend(spam_results.get('sources', []))
            
            # Add risk factors based on spam reports
            if spam_results.get('total_reports', 0) > 0:
                severity = 'HIGH' if spam_results['total_reports'] > 10 else 'MEDIUM'
                self.results['risk_factors'].append({
                    'category': 'spam_reports',
                    'factor_type': 'reported_spam',
                    'severity': severity,
                    'weight': 0.25,
                    'description': f"Number reported {spam_results['total_reports']} times in spam databases",
                    'evidence': spam_results,
                    'source': 'Spam Databases'
                })
                
        except Exception as e:
            self.results['spam_check_error'] = str(e)
    
    def _check_fraud_forums(self):
        """Check fraud forums and dark web mentions"""
        try:
            scanner = FraudForumScanner(self.phone_number)
            fraud_results = scanner.scan()
            
            self.results['fraud_mentions_count'] = fraud_results.get('mentions_count', 0)
            self.results['fraud_details'] = fraud_results.get('mentions', [])
            self.results['data_sources_used'].extend(['fraud_forum_scan'])
            
            # Add risk factors if found in fraud forums
            if fraud_results.get('mentions_count', 0) > 0:
                self.results['risk_factors'].append({
                    'category': 'fraud_forum',
                    'factor_type': 'fraud_mention',
                    'severity': 'HIGH',
                    'weight': 0.25,
                    'description': f"Number mentioned in {fraud_results['mentions_count']} fraud-related discussions",
                    'evidence': fraud_results,
                    'source': 'Fraud Forums'
                })
                
        except Exception as e:
            self.results['fraud_scan_error'] = str(e)
    
    def _check_messaging_apps(self):
        """Check Telegram and WhatsApp presence"""
        try:
            # Telegram scan
            telegram_scanner = TelegramScanner(self.phone_number)
            telegram_results = telegram_scanner.scan()
            self.results['telegram_presence'] = telegram_results
            
            # WhatsApp check
            whatsapp_checker = WhatsAppChecker(self.phone_number)
            whatsapp_results = whatsapp_checker.check()
            self.results['whatsapp_presence'] = whatsapp_results
            
            self.results['data_sources_used'].extend(['telegram_scan', 'whatsapp_check'])
            
            # Add risk factors for suspicious messaging app activity
            if telegram_results.get('suspicious_groups'):
                self.results['risk_factors'].append({
                    'category': 'messaging_apps',
                    'factor_type': 'suspicious_telegram_activity',
                    'severity': 'MEDIUM',
                    'weight': 0.10,
                    'description': f"Found in {len(telegram_results['suspicious_groups'])} suspicious Telegram groups",
                    'evidence': telegram_results,
                    'source': 'Telegram'
                })
                
        except Exception as e:
            self.results['messaging_apps_error'] = str(e)
    
    def _calculate_risk(self):
        """Calculate overall risk score"""
        scorer = RiskScorer(self.results)
        risk_score, risk_level = scorer.calculate()
        
        self.results['risk_score'] = risk_score
        self.results['risk_level'] = risk_level
        
        # Add score contribution to each risk factor
        for factor in self.results['risk_factors']:
            factor['score_contribution'] = scorer.get_factor_contribution(factor)
