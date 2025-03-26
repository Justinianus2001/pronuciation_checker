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

    # Set environment variables
    os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
