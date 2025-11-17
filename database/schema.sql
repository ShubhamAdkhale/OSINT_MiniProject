-- OSINT Fraud Detection Database Schema
-- PostgreSQL

-- Create database
-- CREATE DATABASE osint_fraud_db;

-- Phone Analyses Table
CREATE TABLE IF NOT EXISTS phone_analyses (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    country_code VARCHAR(5),
    carrier VARCHAR(100),
    line_type VARCHAR(50),
    
    -- Risk Assessment
    risk_score FLOAT DEFAULT 0.0,
    risk_level VARCHAR(20) CHECK (risk_level IN ('MINIMAL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    
    -- OSINT Findings
    social_media_presence JSONB,
    spam_reports_count INTEGER DEFAULT 0,
    fraud_mentions_count INTEGER DEFAULT 0,
    telegram_presence JSONB,
    whatsapp_presence JSONB,
    
    -- Metadata
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_duration FLOAT,
    data_sources_used JSONB,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_phone_number (phone_number),
    INDEX idx_risk_level (risk_level),
    INDEX idx_analysis_date (analysis_date)
);

-- Risk Factors Table
CREATE TABLE IF NOT EXISTS risk_factors (
    id SERIAL PRIMARY KEY,
    analysis_id INTEGER NOT NULL REFERENCES phone_analyses(id) ON DELETE CASCADE,
    
    category VARCHAR(100) NOT NULL,
    factor_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    weight FLOAT DEFAULT 1.0,
    score_contribution FLOAT DEFAULT 0.0,
    
    description TEXT,
    evidence JSONB,
    source VARCHAR(200),
    
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_analysis_id (analysis_id),
    INDEX idx_category (category),
    INDEX idx_severity (severity)
);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for phone_analyses
CREATE TRIGGER update_phone_analyses_updated_at
    BEFORE UPDATE ON phone_analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample queries for reference

-- Get high risk numbers
-- SELECT phone_number, risk_score, risk_level 
-- FROM phone_analyses 
-- WHERE risk_level IN ('HIGH', 'CRITICAL')
-- ORDER BY risk_score DESC;

-- Get analysis with risk factors
-- SELECT pa.*, rf.*
-- FROM phone_analyses pa
-- LEFT JOIN risk_factors rf ON pa.id = rf.analysis_id
-- WHERE pa.id = 1;

-- Get statistics
-- SELECT 
--     COUNT(*) as total_analyses,
--     COUNT(CASE WHEN risk_level = 'HIGH' THEN 1 END) as high_risk,
--     COUNT(CASE WHEN risk_level = 'MEDIUM' THEN 1 END) as medium_risk,
--     COUNT(CASE WHEN risk_level = 'LOW' THEN 1 END) as low_risk,
--     AVG(risk_score) as avg_risk_score
-- FROM phone_analyses;
