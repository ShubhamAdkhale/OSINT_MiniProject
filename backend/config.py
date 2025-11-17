import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///osint_fraud.db'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # API Keys
    NUMVERIFY_API_KEY = os.environ.get('NUMVERIFY_API_KEY', '')
    TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID', '')
    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH', '')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    
    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # OSINT Settings
    MAX_SOCIAL_SEARCH_DEPTH = 3
    REQUEST_TIMEOUT = 30
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    # Risk Scoring Weights
    RISK_WEIGHTS = {
        'social_media_anomalies': 0.30,
        'spam_reports': 0.25,
        'fraud_forum_mentions': 0.25,
        'account_age': 0.10,
        'geographic_anomalies': 0.10
    }
    
    # Thresholds
    HIGH_RISK_THRESHOLD = 70
    MEDIUM_RISK_THRESHOLD = 40
    
    # Report Settings
    REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')
    MAX_REPORT_AGE_DAYS = 90

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
