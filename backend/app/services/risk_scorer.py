"""
Risk Scoring Algorithm

Calculates risk scores based on multiple factors with weighted contributions.
"""

from typing import Dict, List, Tuple
from flask import current_app

class RiskScorer:
    """Calculate risk scores for phone number analysis"""
    
    def __init__(self, analysis_results: Dict):
        self.results = analysis_results
        self.weights = {
            'social_media_anomalies': 0.30,
            'spam_reports': 0.25,
            'fraud_forum_mentions': 0.25,
            'account_age': 0.10,
            'geographic_anomalies': 0.10
        }
        self.risk_factors = analysis_results.get('risk_factors', [])
    
    def calculate(self) -> Tuple[float, str]:
        """
        Calculate overall risk score and level
        
        Returns:
            tuple: (risk_score, risk_level)
        """
        total_score = 0.0
        
        # Calculate scores for each category
        social_score = self._calculate_social_media_score()
        spam_score = self._calculate_spam_score()
        fraud_score = self._calculate_fraud_score()
        age_score = self._calculate_account_age_score()
        geo_score = self._calculate_geographic_score()
        
        # Apply weights
        total_score = (
            social_score * self.weights['social_media_anomalies'] +
            spam_score * self.weights['spam_reports'] +
            fraud_score * self.weights['fraud_forum_mentions'] +
            age_score * self.weights['account_age'] +
            geo_score * self.weights['geographic_anomalies']
        )
        
        # Normalize to 0-100
        total_score = min(100.0, max(0.0, total_score))
        
        # Determine risk level
        risk_level = self._determine_risk_level(total_score)
        
        return round(total_score, 2), risk_level
    
    def _calculate_social_media_score(self) -> float:
        """Calculate score based on social media anomalies"""
        social_data = self.results.get('social_media_presence', {})
        score = 0.0
        
        # Check for anomalies
        if social_data.get('anomaly_detected'):
            accounts_found = len(social_data.get('accounts_found', []))
            
            # Multiple recent accounts is suspicious
            recent_accounts = [
                acc for acc in social_data.get('accounts_found', [])
                if acc.get('account_age_days', 999) < 30
            ]
            
            if len(recent_accounts) >= 3:
                score += 80
            elif len(recent_accounts) >= 2:
                score += 60
            elif len(recent_accounts) == 1:
                score += 30
            
            # No accounts found is also suspicious
            if accounts_found == 0:
                score += 20
            
            # Too many accounts is suspicious
            if accounts_found > 5:
                score += 40
        
        return min(100.0, score)
    
    def _calculate_spam_score(self) -> float:
        """Calculate score based on spam reports"""
        spam_count = self.results.get('spam_reports_count', 0)
        
        if spam_count == 0:
            return 0.0
        elif spam_count <= 3:
            return 30.0
        elif spam_count <= 10:
            return 60.0
        elif spam_count <= 20:
            return 85.0
        else:
            return 100.0
    
    def _calculate_fraud_score(self) -> float:
        """Calculate score based on fraud forum mentions"""
        fraud_count = self.results.get('fraud_mentions_count', 0)
        
        if fraud_count == 0:
            return 0.0
        elif fraud_count == 1:
            return 50.0
        elif fraud_count <= 3:
            return 80.0
        else:
            return 100.0
    
    def _calculate_account_age_score(self) -> float:
        """Calculate score based on account ages"""
        social_data = self.results.get('social_media_presence', {})
        accounts = social_data.get('accounts_found', [])
        
        if not accounts:
            return 30.0  # No accounts found is mildly suspicious
        
        # Calculate average account age
        ages = [acc.get('account_age_days', 0) for acc in accounts]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        # Very new accounts are suspicious
        if avg_age < 7:
            return 90.0
        elif avg_age < 30:
            return 70.0
        elif avg_age < 90:
            return 40.0
        elif avg_age < 180:
            return 20.0
        else:
            return 0.0
    
    def _calculate_geographic_score(self) -> float:
        """Calculate score based on geographic anomalies"""
        # In a full implementation, this would check:
        # - Multiple locations for same number
        # - Unusual country codes
        # - VPN/proxy usage indicators
        # - Location changes in short time periods
        
        location = self.results.get('location', 'Unknown')
        
        # Placeholder logic
        if location == 'Unknown':
            return 20.0
        
        return 0.0
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on score"""
        if score >= 70:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        elif score >= 20:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def get_factor_contribution(self, factor: Dict) -> float:
        """Calculate how much a specific factor contributes to total score"""
        category = factor.get('category')
        weight = factor.get('weight', 1.0)
        severity = factor.get('severity', 'MEDIUM')
        
        # Base score from severity
        severity_scores = {
            'CRITICAL': 100,
            'HIGH': 80,
            'MEDIUM': 50,
            'LOW': 25
        }
        
        base_score = severity_scores.get(severity, 50)
        
        # Apply weight
        contribution = base_score * weight
        
        return round(contribution, 2)
    
    def get_detailed_breakdown(self) -> Dict:
        """Get detailed breakdown of risk scoring"""
        return {
            'total_score': self.calculate()[0],
            'risk_level': self.calculate()[1],
            'category_scores': {
                'social_media': self._calculate_social_media_score(),
                'spam_reports': self._calculate_spam_score(),
                'fraud_forums': self._calculate_fraud_score(),
                'account_age': self._calculate_account_age_score(),
                'geographic': self._calculate_geographic_score()
            },
            'weights': self.weights,
            'factor_contributions': [
                {
                    'factor': rf.get('factor_type'),
                    'contribution': self.get_factor_contribution(rf)
                }
                for rf in self.risk_factors
            ]
        }
