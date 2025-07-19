"""
Trace-AI Flask Application Factory
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import logging
from app.config import Config
from app.database import init_db
from app.swagger import swagger_config


def create_app(config_class=Config):
    """Create Flask application instance"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object(config_class)
    
    # Setup logging
    if not app.config.get('TESTING'):
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app.logger.setLevel(logging.INFO)
        app.logger.info("Trace-AI application starting...")
    
    # Initialize database
    init_db(app.config['DB_PATH'])
    if not app.config.get('TESTING'):
        app.logger.info(f"Database initialized: {app.config['DB_PATH']}")
    
    # Request logging
    @app.after_request
    def log_request(response):
        if not app.config.get('TESTING'):
            app.logger.info(f"{request.method} {request.path} - {request.remote_addr} - {response.status_code}")
        return response
    
    # Swagger spec endpoint
    @app.route('/swagger.json')
    def swagger():
        return jsonify(swagger_config)
    
    # Register blueprints
    from app.routes import logs_bp
    app.register_blueprint(logs_bp)
    
    # Swagger UI
    swagger_ui = get_swaggerui_blueprint(
        '/docs',
        '/swagger.json',
        config={'app_name': "Trace-AI API"}
    )
    app.register_blueprint(swagger_ui)
    
    if not app.config.get('TESTING'):
        app.logger.info("Application initialized successfully")
    
    return app