from datetime import datetime
from app import db
import json

class PhoneAnalysis(db.Model):
    __tablename__ = 'phone_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    country_code = db.Column(db.String(5))
    carrier = db.Column(db.String(100))
    line_type = db.Column(db.String(50))
    
    # Risk Assessment
    risk_score = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    
    # OSINT Findings
    social_media_presence = db.Column(db.JSON)
    spam_reports_count = db.Column(db.Integer, default=0)
    fraud_mentions_count = db.Column(db.Integer, default=0)
    telegram_presence = db.Column(db.JSON)
    whatsapp_presence = db.Column(db.JSON)
    
    # Rich Metadata (Enhanced)
    rich_metadata = db.Column(db.JSON)  # Carrier history, geographic data, number status
    
    # Metadata
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    analysis_duration = db.Column(db.Float)  # in seconds
    data_sources_used = db.Column(db.JSON)
    
    # Relationships
    risk_factors = db.relationship('RiskFactor', backref='analysis', lazy='dynamic', cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'country_code': self.country_code,
            'carrier': self.carrier,
            'line_type': self.line_type,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'social_media_presence': self.social_media_presence or {},
            'spam_reports_count': self.spam_reports_count,
            'fraud_mentions_count': self.fraud_mentions_count,
            'telegram_presence': self.telegram_presence or {},
            'whatsapp_presence': self.whatsapp_presence or {},
            'rich_metadata': self.rich_metadata or {},  # Enhanced metadata
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'analysis_duration': self.analysis_duration,
            'data_sources_used': self.data_sources_used or [],
            'risk_factors': [rf.to_dict() for rf in self.risk_factors],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PhoneAnalysis {self.phone_number} - Risk: {self.risk_level}>'
