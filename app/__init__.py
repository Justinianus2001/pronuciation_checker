from app.config import Config
from flask import Flask, jsonify
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize rate limiter
    if app.config.get('RATELIMIT_ENABLED', True):
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
        
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            storage_uri=app.config.get('RATELIMIT_STORAGE_URI', 'memory://'),
            strategy=app.config.get('RATELIMIT_STRATEGY', 'fixed-window'),
            default_limits=[],  # No default limits, we'll set per-endpoint
            headers_enabled=True,  # Add rate limit headers to responses
        )
        
        # Custom error handler for rate limit exceeded
        @app.errorhandler(429)
        def ratelimit_handler(e):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. This is a demo application with limited API credits. Please try again later.',
                'limit': str(e.description) if hasattr(e, 'description') else 'Rate limit exceeded',
            }), 429
        
        # Store limiter in app context for use in routes
        app.limiter = limiter
    else:
        app.limiter = None

    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Initialize cleanup scheduler
    if app.config.get('CLEANUP_ENABLED', True):
        from app.services.scheduler import init_scheduler
        init_scheduler(app)

    return app