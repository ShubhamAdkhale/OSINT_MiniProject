from datetime import datetime
from app import db

class RiskFactor(db.Model):
    __tablename__ = 'risk_factors'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('phone_analyses.id'), nullable=False)
    
    category = db.Column(db.String(100), nullable=False)  # e.g., 'social_media', 'spam', 'fraud_forum'
    factor_type = db.Column(db.String(100), nullable=False)  # specific indicator
    severity = db.Column(db.String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    weight = db.Column(db.Float, default=1.0)
    score_contribution = db.Column(db.Float, default=0.0)
    
    description = db.Column(db.Text)
    evidence = db.Column(db.JSON)  # Store evidence data
    source = db.Column(db.String(200))  # Data source URL or name
    
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'factor_type': self.factor_type,
            'severity': self.severity,
            'weight': self.weight,
            'score_contribution': self.score_contribution,
            'description': self.description,
            'evidence': self.evidence or {},
            'source': self.source,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None
        }
    
    def __repr__(self):
        return f'<RiskFactor {self.factor_type} - {self.severity}>'
