"""
Self-Consistency API Endpoints
Flask blueprint for self-consistency validation techniques
"""

import asyncio
import logging
from flask import Blueprint, request, jsonify
from core.prompting_service import get_prompting_service
from utils.response_formatter import format_technique_response, format_error_response, format_validation_error
from utils.validators import (
    validate_self_consistency_validate,
    validate_json_content_type,
    validate_request_size
)

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
self_consistency_bp = Blueprint('self_consistency', __name__)


@self_consistency_bp.before_request
def validate_request():
    """Validate request before processing"""
    # Check content type for POST requests
    if request.method == 'POST':
        content_type_error = validate_json_content_type(request)
        if content_type_error:
            return jsonify(format_error_response("INVALID_CONTENT_TYPE", content_type_error)), 400
        
        # Check request size
        size_error = validate_request_size(request, max_size_mb=1)
        if size_error:
            return jsonify(format_error_response("REQUEST_TOO_LARGE", size_error)), 413


@self_consistency_bp.route('/validate', methods=['POST'])
def validate_consistency():
    """
    Get consistent answers using multiple sampling and validation
    
    Expected JSON payload:
    {
        "question": "Question to answer with consistency validation",
        "num_samples": 3  // Optional, defaults to 3
    }
    """
    try:
        data = request.get_json()
        
        # Validate request data
        validation_errors = validate_self_consistency_validate(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Set default num_samples if not provided
        num_samples = data.get('num_samples', 3)
        
        # Run self-consistency validation (async)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                service.self_consistency_validate(data['question'], num_samples)
            )
        finally:
            loop.close()
        
        logger.info(f"Self-consistency validation completed for: {data['question'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Self-consistency validation failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("SELF_CONSISTENCY_FAILED", str(e))), 500


@self_consistency_bp.route('/info', methods=['GET'])
def self_consistency_info():
    """Get information about self-consistency endpoints"""
    info_data = {
        "technique": "Self-Consistency",
        "description": "Generate multiple responses and aggregate for better accuracy and reliability",
        "endpoints": {
            "validate": {
                "method": "POST",
                "description": "Get consistent answers using multiple sampling",
                "required_fields": ["question"],
                "optional_fields": ["num_samples"],
                "example": {
                    "question": "What are the main benefits of renewable energy?",
                    "num_samples": 3
                }
            }
        },
        "features": [
            "Multiple response generation",
            "Consistency analysis",
            "Majority voting aggregation",
            "Reliability scoring"
        ],
        "parameters": {
            "num_samples": {
                "description": "Number of responses to generate for consistency check",
                "type": "integer",
                "default": 3,
                "range": "2-5"
            }
        },
        "benefits": [
            "Reduces hallucinations",
            "Increases answer reliability",
            "Provides confidence scoring",
            "Identifies inconsistencies"
        ]
    }
    
    return jsonify(format_technique_response({
        "technique": "Self-Consistency",
        "task": "info",
        "input": "endpoint_information",
        "output": info_data,
        "metadata": {"processing_time": 0.001, "model": "info"}
    }))


# Error handlers for this blueprint
@self_consistency_bp.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify(format_error_response("BAD_REQUEST", "Invalid request data")), 400


@self_consistency_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify(format_error_response("METHOD_NOT_ALLOWED", "Method not allowed for this endpoint")), 405


@self_consistency_bp.errorhandler(413)
def request_too_large(error):
    """Handle request too large errors"""
    return jsonify(format_error_response("REQUEST_TOO_LARGE", "Request payload too large")), 413