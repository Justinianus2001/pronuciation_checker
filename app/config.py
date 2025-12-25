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

    # Set environment variables
    os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
