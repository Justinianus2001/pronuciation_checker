from app.config import Config
from flask import Flask
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Initialize cleanup scheduler
    if app.config.get('CLEANUP_ENABLED', True):
        from app.services.scheduler import init_scheduler
        init_scheduler(app)

    return app