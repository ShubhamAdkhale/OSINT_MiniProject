from flask import Blueprint, request, jsonify
from app import db, limiter
from app.models.phone_analysis import PhoneAnalysis
from app.services.phone_analyzer import PhoneAnalyzer
from app.utils.validators import validate_phone_number
import time

bp = Blueprint('analysis', __name__, url_prefix='/api')

@bp.route('/analyze', methods=['POST'])
@limiter.limit("10 per hour")
def analyze_phone():
    """
    Analyze a phone number for fraud indicators
    
    Request Body:
    {
        "phone_number": "+1234567890",
        "deep_scan": false
    }
    """
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        deep_scan = data.get('deep_scan', False)
        
        # Validate phone number
        is_valid, error_msg = validate_phone_number(phone_number)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Check if recent analysis exists (within 24 hours)
        from datetime import datetime, timedelta
        recent_analysis = PhoneAnalysis.query.filter_by(
            phone_number=phone_number
        ).filter(
            PhoneAnalysis.analysis_date > datetime.utcnow() - timedelta(hours=24)
        ).first()
        
        if recent_analysis and not deep_scan:
            return jsonify({
                'message': 'Using cached analysis from last 24 hours',
                'analysis': recent_analysis.to_dict()
            }), 200
        
        # Perform new analysis
        start_time = time.time()
        analyzer = PhoneAnalyzer(phone_number, deep_scan=deep_scan)
        analysis_result = analyzer.analyze()
        duration = time.time() - start_time
        
        # Save to database
        analysis = PhoneAnalysis(
            phone_number=phone_number,
            country_code=analysis_result.get('country_code'),
            carrier=analysis_result.get('carrier'),
            line_type=analysis_result.get('line_type'),
            risk_score=analysis_result.get('risk_score'),
            risk_level=analysis_result.get('risk_level'),
            social_media_presence=analysis_result.get('social_media_presence'),
            spam_reports_count=analysis_result.get('spam_reports_count'),
            fraud_mentions_count=analysis_result.get('fraud_mentions_count'),
            telegram_presence=analysis_result.get('telegram_presence'),
            whatsapp_presence=analysis_result.get('whatsapp_presence'),
            rich_metadata=analysis_result.get('rich_metadata'),  # Enhanced metadata
            analysis_duration=duration,
            data_sources_used=analysis_result.get('data_sources_used')
        )
        
        db.session.add(analysis)
        
        # Add risk factors
        from app.models.risk_factor import RiskFactor
        for factor in analysis_result.get('risk_factors', []):
            risk_factor = RiskFactor(
                analysis=analysis,
                category=factor.get('category'),
                factor_type=factor.get('factor_type'),
                severity=factor.get('severity'),
                weight=factor.get('weight'),
                score_contribution=factor.get('score_contribution'),
                description=factor.get('description'),
                evidence=factor.get('evidence'),
                source=factor.get('source')
            )
            db.session.add(risk_factor)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'analysis': analysis.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/report/<int:analysis_id>', methods=['GET'])
def get_report(analysis_id):
    """Get detailed analysis report by ID"""
    try:
        analysis = PhoneAnalysis.query.get_or_404(analysis_id)
        return jsonify(analysis.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_history():
    """Get analysis history with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        analyses = PhoneAnalysis.query.order_by(
            PhoneAnalysis.analysis_date.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'analyses': [analysis.to_dict() for analysis in analyses.items],
            'total': analyses.total,
            'pages': analyses.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['POST'])
def search_analyses():
    """Search analyses by phone number or risk level"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        risk_level = data.get('risk_level')
        
        query = PhoneAnalysis.query
        
        if phone_number:
            query = query.filter(PhoneAnalysis.phone_number.contains(phone_number))
        
        if risk_level:
            query = query.filter_by(risk_level=risk_level.upper())
        
        analyses = query.order_by(PhoneAnalysis.analysis_date.desc()).all()
        
        return jsonify({
            'count': len(analyses),
            'analyses': [analysis.to_dict() for analysis in analyses]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/report/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Delete a specific analysis by ID"""
    try:
        analysis = PhoneAnalysis.query.get_or_404(analysis_id)
        
        # Delete associated risk factors first
        from app.models.risk_factor import RiskFactor
        RiskFactor.query.filter_by(analysis_id=analysis_id).delete()
        
        # Delete the analysis
        db.session.delete(analysis)
        db.session.commit()
        
        return jsonify({
            'message': 'Analysis deleted successfully',
            'id': analysis_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/history/clear', methods=['DELETE'])
def clear_all_history():
    """Delete all analysis history"""
    try:
        # Delete all risk factors first
        from app.models.risk_factor import RiskFactor
        RiskFactor.query.delete()
        
        # Delete all analyses
        count = PhoneAnalysis.query.delete()
        db.session.commit()
        
        return jsonify({
            'message': f'All analysis history cleared successfully',
            'deleted_count': count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get overall statistics"""
    try:
        total_analyses = PhoneAnalysis.query.count()
        high_risk = PhoneAnalysis.query.filter_by(risk_level='HIGH').count()
        medium_risk = PhoneAnalysis.query.filter_by(risk_level='MEDIUM').count()
        low_risk = PhoneAnalysis.query.filter_by(risk_level='LOW').count()
        
        return jsonify({
            'total_analyses': total_analyses,
            'high_risk_count': high_risk,
            'medium_risk_count': medium_risk,
            'low_risk_count': low_risk,
            'risk_distribution': {
                'high': high_risk,
                'medium': medium_risk,
                'low': low_risk
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
