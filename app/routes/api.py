import base64
from app.services.ai_agent import (
    analyze_pronunciation, 
    evaluate_speech_metrics,
    generate_speaking_report,
)
from app.utils.file_utils import allowed_file
from app.utils.cleanup import FileCleanupService
from flask import Blueprint, request, jsonify, current_app


bp = Blueprint('api', __name__)

def get_limiter():
    """Get the limiter instance from current app"""
    return current_app.limiter if hasattr(current_app, 'limiter') and current_app.limiter else None

def limit_decorator(limit_string):
    """Decorator factory that applies rate limit if limiter is enabled"""
    def decorator(f):
        limiter = get_limiter()
        if limiter:
            return limiter.limit(limit_string)(f)
        return f
    return decorator

@bp.route('/analyze-pronunciation-error', methods=['POST'])
def analyze():
    """
    Analyze pronunciation errors in audio.
    Rate limit: 10 requests per hour (expensive AI operation)
    """
    # Apply rate limit dynamically
    limiter = get_limiter()
    if limiter:
        limit_string = current_app.config.get('RATELIMIT_AI_ENDPOINTS', '10 per hour')
        limiter.limit(limit_string)(lambda: None)()
    
    # Validate request
    if 'audio' not in request.files:
        return jsonify({'error': 'Missing audio file'}), 400

    if 'text' not in request.form:
        return jsonify({'error': 'Missing text'}), 400
    
    audio_file = request.files['audio']
    reference_text = request.form['text']

    if not allowed_file(audio_file.filename):
        return jsonify({'error': 'Invalid file type'}), 400


    try:
        base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        # Save uploaded file
        # audio_path = save_uploaded_file(audio_file)
        
        # Process with AI Agent
        result = analyze_pronunciation(reference_text, base64_audio)
        
        return jsonify({
            'data': result,
            'status': 'success',
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@bp.route('/evaluate-speech-metrics', methods=['POST'])
def evaluate():
    """
    Evaluate speech metrics (IELTS scoring).
    Rate limit: 10 requests per hour (expensive AI operation)
    """
    # Apply rate limit dynamically
    limiter = get_limiter()
    if limiter:
        limit_string = current_app.config.get('RATELIMIT_AI_ENDPOINTS', '10 per hour')
        limiter.limit(limit_string)(lambda: None)()
    
    # Validate request
    if 'audio' not in request.files:
        return jsonify({'error': 'Missing audio file'}), 400

    if 'text' not in request.form:
        return jsonify({'error': 'Missing text'}), 400
    
    audio_file = request.files['audio']
    reference_text = request.form['text']

    if not allowed_file(audio_file.filename):
        return jsonify({'error': 'Invalid file type'}), 400


    try:
        base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        # Save uploaded file
        # audio_path = save_uploaded_file(audio_file)
        
        # Process with AI Agent
        result = evaluate_speech_metrics(reference_text, base64_audio)
        
        return jsonify({
            'data': result,
            'status': 'success',
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@bp.route('/generate-speaking-report', methods=['POST'])
def summary():
    """
    Generate speaking performance report.
    Rate limit: 20 requests per hour (moderate cost)
    """
    # Apply rate limit dynamically
    limiter = get_limiter()
    if limiter:
        limit_string = current_app.config.get('RATELIMIT_REPORT_ENDPOINT', '20 per hour')
        limiter.limit(limit_string)(lambda: None)()
    
    if 'text' not in request.form:
        return jsonify({'error': 'Missing text'}), 400
    
    test_results = request.form['text']
    try:
        result = generate_speaking_report(test_results)
        return jsonify({
            'data': result,
            'status': 'success',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/health-check', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Rate limit: 100 requests per hour (utility endpoint)
    """
    # Apply rate limit dynamically
    limiter = get_limiter()
    if limiter:
        limit_string = current_app.config.get('RATELIMIT_UTILITY_ENDPOINTS', '100 per hour')
        limiter.limit(limit_string)(lambda: None)()
    
    return jsonify({'status': 'ok'}), 200


@bp.route('/storage-stats', methods=['GET'])
def storage_stats():
    """
    Get current storage statistics.
    Rate limit: 100 requests per hour (utility endpoint)
    """
    # Apply rate limit dynamically
    limiter = get_limiter()
    if limiter:
        limit_string = current_app.config.get('RATELIMIT_UTILITY_ENDPOINTS', '100 per hour')
        limiter.limit(limit_string)(lambda: None)()
    
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
        cleanup_service = FileCleanupService(upload_folder)
        stats = cleanup_service.get_storage_stats()
        
        return jsonify({
            'status': 'success',
            'data': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/cleanup-uploads', methods=['POST'])
def cleanup_uploads():
    """
    Manually trigger cleanup of old uploads.
    Rate limit: 100 requests per hour (utility endpoint)
    """
    # Apply rate limit dynamically
    limiter = get_limiter()
    if limiter:
        limit_string = current_app.config.get('RATELIMIT_UTILITY_ENDPOINTS', '100 per hour')
        limiter.limit(limit_string)(lambda: None)()
    
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
        max_age_days = request.json.get('max_age_days', 7) if request.json else 7
        
        cleanup_service = FileCleanupService(upload_folder, max_age_days)
        result = cleanup_service.cleanup_old_files()
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500