from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'OSINT Fraud Detection API',
        'version': '1.0.0'
    }), 200

@bp.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint with service details"""
    return jsonify({
        'status': 'online',
        'endpoints': {
            'analyze': '/api/analyze',
            'report': '/api/report/<id>',
            'history': '/api/history',
            'search': '/api/search',
            'statistics': '/api/statistics'
        },
        'rate_limits': {
            'analyze': '10 per hour',
            'default': '200 per day'
        }
    }), 200
