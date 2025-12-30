import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or './uploads'
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'webm'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Cleanup configuration
    CLEANUP_ENABLED = os.environ.get('CLEANUP_ENABLED', 'true').lower() == 'true'
    CLEANUP_MAX_AGE_DAYS = int(os.environ.get('CLEANUP_MAX_AGE_DAYS', '7'))
    CLEANUP_INTERVAL_HOURS = int(os.environ.get('CLEANUP_INTERVAL_HOURS', '24'))
    
    # Rate limiting configuration
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'true').lower() == 'true'
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_STRATEGY = os.environ.get('RATELIMIT_STRATEGY', 'fixed-window')
    
    # Rate limits for different endpoint categories
    # AI endpoints (most expensive - consume Google API credits)
    RATELIMIT_AI_ENDPOINTS = os.environ.get('RATELIMIT_AI_ENDPOINTS', '10 per hour')
    # Report generation (moderate cost)
    RATELIMIT_REPORT_ENDPOINT = os.environ.get('RATELIMIT_REPORT_ENDPOINT', '20 per hour')
    # Utility endpoints (health checks, stats)
    RATELIMIT_UTILITY_ENDPOINTS = os.environ.get('RATELIMIT_UTILITY_ENDPOINTS', '100 per hour')

    # Set environment variables
    os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
