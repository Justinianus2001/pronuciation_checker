from app.config import Config
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app