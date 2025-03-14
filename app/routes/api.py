from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
import os
from app.services.ai_agent import (
    analyze_pronunciation, 
    evaluate_speech_metrics,
    generate_speaking_report
)
from app.utils.file_utils import allowed_file, save_uploaded_file
import base64


bp = Blueprint('api', __name__)

@bp.route('/analyze-pronunciation-error', methods=['POST'])
def analyze():
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
        audio_path = save_uploaded_file(audio_file)
        
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
        audio_path = save_uploaded_file(audio_file)
        
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
    return jsonify({'status': 'ok'}), 200