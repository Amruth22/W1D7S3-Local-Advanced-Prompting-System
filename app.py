"""
Local Advanced Prompting System - Flask API
Main Flask application entry point
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv

from core.gemini_client import initialize_gemini_client
from core.prompting_service import get_prompting_service
from utils.response_formatter import format_success_response, format_error_response
from utils.validators import validate_request_data

# Import API blueprints
from api.few_shot import few_shot_bp
from api.chain_of_thought import chain_of_thought_bp
from api.tree_of_thought import tree_of_thought_bp
from api.self_consistency import self_consistency_bp
from api.meta_prompting import meta_prompting_bp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Local Advanced Prompting System API",
        "description": "A comprehensive Flask API for advanced prompting techniques with local deployment capabilities.",
        "contact": {
            "name": "API Support",
            "url": "https://github.com/Amruth22/Local-Advanced-Prompting-System"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/api/v1",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
}


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.config['TESTING'] = False
    
    # Enable CORS
    CORS(app, origins="*")
    
    # Initialize Swagger UI
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    
    # Initialize Gemini client
    try:
        initialize_gemini_client()
        logger.info("Gemini client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        # Don't exit - let the app start and show proper error messages
    
    # Register blueprints
    api_prefix = os.getenv('API_PREFIX', '/api')
    api_version = os.getenv('API_VERSION', 'v1')
    base_url = f"{api_prefix}/{api_version}"
    
    app.register_blueprint(few_shot_bp, url_prefix=f"{base_url}/few-shot")
    app.register_blueprint(chain_of_thought_bp, url_prefix=f"{base_url}/chain-of-thought")
    app.register_blueprint(tree_of_thought_bp, url_prefix=f"{base_url}/tree-of-thought")
    app.register_blueprint(self_consistency_bp, url_prefix=f"{base_url}/self-consistency")
    app.register_blueprint(meta_prompting_bp, url_prefix=f"{base_url}/meta-prompting")
    
    # Health check endpoint
    @app.route(f"{api_prefix}/health")
    def health_check():
        """
        Health Check Endpoint
        ---
        tags:
          - System
        responses:
          200:
            description: System is healthy
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "healthy"
                    services:
                      type: object
                      properties:
                        flask_app:
                          type: boolean
                          example: true
                        gemini_api:
                          type: boolean
                          example: true
                        prompting_service:
                          type: boolean
                          example: true
          503:
            description: System is unhealthy
        """
        try:
            service = get_prompting_service()
            gemini_test = service.gemini_client.test_connection()
            
            health_status = {
                "status": "healthy" if gemini_test["gemini_api"] else "degraded",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
                "services": {
                    "flask_app": True,
                    "gemini_api": gemini_test["gemini_api"],
                    "prompting_service": True
                },
                "model_info": service.gemini_client.get_model_info()
            }
            
            status_code = 200 if health_status["status"] == "healthy" else 503
            return jsonify(format_success_response(health_status)), status_code
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            error_response = {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
            return jsonify(format_error_response("HEALTH_CHECK_FAILED", str(e))), 503
    
    # API info endpoint
    @app.route(f"{api_prefix}/info")
    def api_info():
        """
        API Information Endpoint
        ---
        tags:
          - System
        responses:
          200:
            description: API information
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    api_name:
                      type: string
                      example: "Local Advanced Prompting System"
                    version:
                      type: string
                      example: "1.0.0"
                    endpoints:
                      type: object
        """
        try:
            service = get_prompting_service()
            info = service.get_service_info()
            
            api_info_data = {
                "api_name": "Local Advanced Prompting System",
                "version": "1.0.0",
                "description": "Flask API for advanced prompting techniques",
                "swagger_ui": "/docs/",
                "endpoints": {
                    "few_shot": [
                        f"{base_url}/few-shot/sentiment",
                        f"{base_url}/few-shot/math",
                        f"{base_url}/few-shot/ner",
                        f"{base_url}/few-shot/classification"
                    ],
                    "chain_of_thought": [
                        f"{base_url}/chain-of-thought/math",
                        f"{base_url}/chain-of-thought/logic",
                        f"{base_url}/chain-of-thought/analysis"
                    ],
                    "tree_of_thought": [
                        f"{base_url}/tree-of-thought/explore"
                    ],
                    "self_consistency": [
                        f"{base_url}/self-consistency/validate"
                    ],
                    "meta_prompting": [
                        f"{base_url}/meta-prompting/optimize",
                        f"{base_url}/meta-prompting/analyze"
                    ]
                },
                "service_info": info
            }
            
            return jsonify(format_success_response(api_info_data))
            
        except Exception as e:
            logger.error(f"API info failed: {e}")
            return jsonify(format_error_response("API_INFO_FAILED", str(e))), 500
    
    # Root endpoint
    @app.route("/")
    def root():
        """
        Root Endpoint
        ---
        tags:
          - System
        responses:
          200:
            description: Welcome message with API information
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
        """
        welcome_data = {
            "message": "Welcome to Local Advanced Prompting System API",
            "version": "1.0.0",
            "documentation": "https://github.com/Amruth22/Local-Advanced-Prompting-System",
            "swagger_ui": "/docs/",
            "health_check": f"{api_prefix}/health",
            "api_info": f"{api_prefix}/info",
            "base_url": base_url,
            "quick_links": {
                "📚 Swagger Documentation": "/docs/",
                "📊 API Information": f"{api_prefix}/info",
                "❤️ Health Check": f"{api_prefix}/health",
                "🧠 Few-shot Sentiment": f"{base_url}/few-shot/sentiment",
                "🔗 Chain-of-Thought Math": f"{base_url}/chain-of-thought/math"
            }
        }
        return jsonify(format_success_response(welcome_data))
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        return jsonify(format_error_response("BAD_REQUEST", "Invalid request data")), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        return jsonify(format_error_response("NOT_FOUND", "Endpoint not found")), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors"""
        return jsonify(format_error_response("METHOD_NOT_ALLOWED", "Method not allowed for this endpoint")), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        logger.error(f"Internal server error: {error}")
        return jsonify(format_error_response("INTERNAL_ERROR", "Internal server error")), 500
    
    # Request logging middleware
    @app.before_request
    def log_request_info():
        """Log request information"""
        if request.endpoint != 'static':
            logger.info(f"{request.method} {request.url} - {request.remote_addr}")
    
    @app.after_request
    def log_response_info(response):
        """Log response information"""
        if request.endpoint != 'static':
            logger.info(f"Response: {response.status_code} - {request.endpoint}")
        return response
    
    return app


def main():
    """Main function to run the Flask application"""
    app = create_app()
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print("🚀 LOCAL ADVANCED PROMPTING SYSTEM API WITH SWAGGER UI")
    print("=" * 60)
    print(f"🌐 Server: http://{host}:{port}")
    print(f"📚 Swagger UI: http://{host}:{port}/docs/")
    print(f"📊 API Info: http://{host}:{port}/api/info")
    print(f"❤️ Health Check: http://{host}:{port}/api/health")
    print(f"🔧 Debug Mode: {debug}")
    print("=" * 60)
    
    logger.info(f"Starting Local Advanced Prompting System API")
    logger.info(f"Server: http://{host}:{port}")
    logger.info(f"Swagger UI: http://{host}:{port}/docs/")
    logger.info(f"Health Check: http://{host}:{port}/api/health")
    logger.info(f"API Info: http://{host}:{port}/api/info")
    logger.info(f"Debug Mode: {debug}")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")


if __name__ == '__main__':
    main()