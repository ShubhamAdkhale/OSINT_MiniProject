"""
Report Generator Module

Generates detailed PDF and JSON reports for phone number analyses.
"""

from datetime import datetime
from typing import Dict
import json
import os
from flask import current_app

class ReportGenerator:
    """Generate analysis reports in various formats"""
    
    def __init__(self, analysis_data: Dict):
        self.analysis = analysis_data
        self.report_dir = current_app.config.get('REPORTS_DIR', 'reports')
        
        # Create reports directory if it doesn't exist
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_json_report(self) -> str:
        """
        Generate JSON report
        
        Returns:
            str: Path to generated report file
        """
        report_data = {
            'report_metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'report_version': '1.0',
                'analysis_id': self.analysis.get('id')
            },
            'executive_summary': self._generate_executive_summary(),
            'phone_information': self._extract_phone_info(),
            'risk_assessment': self._extract_risk_assessment(),
            'osint_findings': self._extract_osint_findings(),
            'detailed_risk_factors': self._extract_risk_factors(),
            'recommendations': self._generate_recommendations(),
            'raw_data': self.analysis
        }
        
        # Generate filename
        phone = self.analysis.get('phone_number', 'unknown').replace('+', '')
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{phone}_{timestamp}.json"
        filepath = os.path.join(self.report_dir, filename)
        
        # Save report
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return filepath
    
    def generate_text_report(self) -> str:
        """
        Generate human-readable text report
        
        Returns:
            str: Path to generated report file
        """
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("OSINT FRAUD DETECTION ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report_lines.append(f"Report ID: {self.analysis.get('id')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("-" * 80)
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 80)
        summary = self._generate_executive_summary()
        report_lines.append(summary['summary_text'])
        report_lines.append("")
        
        # Phone Information
        report_lines.append("-" * 80)
        report_lines.append("PHONE NUMBER INFORMATION")
        report_lines.append("-" * 80)
        phone_info = self._extract_phone_info()
        for key, value in phone_info.items():
            report_lines.append(f"{key.replace('_', ' ').title()}: {value}")
        report_lines.append("")
        
        # Risk Assessment
        report_lines.append("-" * 80)
        report_lines.append("RISK ASSESSMENT")
        report_lines.append("-" * 80)
        risk = self._extract_risk_assessment()
        report_lines.append(f"Risk Score: {risk['risk_score']}/100")
        report_lines.append(f"Risk Level: {risk['risk_level']}")
        report_lines.append(f"Threat Category: {risk.get('threat_category', 'Unknown')}")
        report_lines.append("")
        
        # Risk Factors
        report_lines.append("-" * 80)
        report_lines.append("DETAILED RISK FACTORS")
        report_lines.append("-" * 80)
        risk_factors = self._extract_risk_factors()
        for i, factor in enumerate(risk_factors, 1):
            report_lines.append(f"\n{i}. {factor['factor_type'].upper()}")
            report_lines.append(f"   Category: {factor['category']}")
            report_lines.append(f"   Severity: {factor['severity']}")
            report_lines.append(f"   Description: {factor['description']}")
            report_lines.append(f"   Score Contribution: {factor['score_contribution']}")
        report_lines.append("")
        
        # OSINT Findings
        report_lines.append("-" * 80)
        report_lines.append("OSINT FINDINGS")
        report_lines.append("-" * 80)
        findings = self._extract_osint_findings()
        for key, value in findings.items():
            if isinstance(value, dict):
                report_lines.append(f"\n{key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    report_lines.append(f"  - {sub_key}: {sub_value}")
            else:
                report_lines.append(f"{key.replace('_', ' ').title()}: {value}")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("-" * 80)
        report_lines.append("RECOMMENDATIONS")
        report_lines.append("-" * 80)
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        report_lines.append("")
        
        # Footer
        report_lines.append("=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)
        
        # Generate filename and save
        phone = self.analysis.get('phone_number', 'unknown').replace('+', '')
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{phone}_{timestamp}.txt"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(report_lines))
        
        return filepath
    
    def _generate_executive_summary(self) -> Dict:
        """Generate executive summary"""
        risk_score = self.analysis.get('risk_score', 0)
        risk_level = self.analysis.get('risk_level', 'UNKNOWN')
        phone = self.analysis.get('phone_number')
        
        summary_text = f"Analysis of phone number {phone} reveals a {risk_level} risk level "
        summary_text += f"with an overall risk score of {risk_score}/100. "
        
        spam_count = self.analysis.get('spam_reports_count', 0)
        fraud_count = self.analysis.get('fraud_mentions_count', 0)
        
        if spam_count > 0:
            summary_text += f"The number has {spam_count} spam report(s). "
        if fraud_count > 0:
            summary_text += f"Found {fraud_count} mention(s) in fraud forums. "
        
        if risk_level in ['HIGH', 'CRITICAL']:
            summary_text += "Immediate investigation recommended."
        elif risk_level == 'MEDIUM':
            summary_text += "Caution advised when engaging with this number."
        else:
            summary_text += "No significant fraud indicators detected."
        
        return {
            'summary_text': summary_text,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'key_findings': {
                'spam_reports': spam_count,
                'fraud_mentions': fraud_count,
                'risk_factors_count': len(self.analysis.get('risk_factors', []))
            }
        }
    
    def _extract_phone_info(self) -> Dict:
        """Extract phone information"""
        return {
            'phone_number': self.analysis.get('phone_number'),
            'country_code': self.analysis.get('country_code'),
            'carrier': self.analysis.get('carrier', 'Unknown'),
            'line_type': self.analysis.get('line_type', 'Unknown'),
            'analysis_date': self.analysis.get('analysis_date'),
            'analysis_duration': f"{self.analysis.get('analysis_duration', 0):.2f}s"
        }
    
    def _extract_risk_assessment(self) -> Dict:
        """Extract risk assessment details"""
        risk_level = self.analysis.get('risk_level', 'UNKNOWN')
        
        threat_categories = {
            'CRITICAL': 'Confirmed Fraud',
            'HIGH': 'Likely Fraud',
            'MEDIUM': 'Suspicious Activity',
            'LOW': 'Minor Concerns',
            'MINIMAL': 'Clean'
        }
        
        return {
            'risk_score': self.analysis.get('risk_score', 0),
            'risk_level': risk_level,
            'threat_category': threat_categories.get(risk_level, 'Unknown')
        }
    
    def _extract_osint_findings(self) -> Dict:
        """Extract OSINT findings"""
        return {
            'spam_reports': self.analysis.get('spam_reports_count', 0),
            'fraud_mentions': self.analysis.get('fraud_mentions_count', 0),
            'social_media_accounts': len(self.analysis.get('social_media_presence', {}).get('accounts_found', [])),
            'data_sources': ', '.join(self.analysis.get('data_sources_used', [])),
            'telegram_presence': 'Yes' if self.analysis.get('telegram_presence', {}).get('has_telegram_account') else 'No',
            'whatsapp_presence': 'Yes' if self.analysis.get('whatsapp_presence', {}).get('has_whatsapp') else 'No'
        }
    
    def _extract_risk_factors(self) -> list:
        """Extract detailed risk factors"""
        return self.analysis.get('risk_factors', [])
    
    def _generate_recommendations(self) -> list:
        """Generate recommendations based on risk level"""
        risk_level = self.analysis.get('risk_level', 'UNKNOWN')
        recommendations = []
        
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.append("Do not engage with this phone number")
            recommendations.append("Block the number immediately")
            recommendations.append("Report to local authorities if contacted")
            recommendations.append("Alert your organization's security team")
        elif risk_level == 'MEDIUM':
            recommendations.append("Exercise caution when engaging with this number")
            recommendations.append("Verify identity through alternative channels")
            recommendations.append("Do not share sensitive information")
            recommendations.append("Monitor for suspicious activity")
        else:
            recommendations.append("Standard verification procedures recommended")
            recommendations.append("Follow normal security protocols")
            recommendations.append("Continue monitoring if concerns arise")
        
        # Add specific recommendations based on findings
        if self.analysis.get('spam_reports_count', 0) > 10:
            recommendations.append("Number has extensive spam history - treat with extreme caution")
        
        if self.analysis.get('fraud_mentions_count', 0) > 0:
            recommendations.append("Number mentioned in fraud forums - consider blocking")
        
        return recommendations
