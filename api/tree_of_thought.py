"""
Tree-of-Thought API Endpoints
Flask blueprint for tree-of-thought exploration techniques
"""

import asyncio
import logging
from flask import Blueprint, request, jsonify
from core.prompting_service import get_prompting_service
from utils.response_formatter import format_technique_response, format_error_response, format_validation_error
from utils.validators import (
    validate_tree_of_thought_explore,
    validate_json_content_type,
    validate_request_size
)

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
tree_of_thought_bp = Blueprint('tree_of_thought', __name__)


@tree_of_thought_bp.before_request
def validate_request():
    """Validate request before processing"""
    # Skip validation for OPTIONS requests (CORS preflight)
    if request.method == 'OPTIONS':
        return
    
    # Check content type for POST requests only
    if request.method == 'POST':
        content_type_error = validate_json_content_type(request)
        if content_type_error:
            return jsonify(format_error_response("INVALID_CONTENT_TYPE", content_type_error)), 400
        
        # Check request size
        size_error = validate_request_size(request, max_size_mb=1)
        if size_error:
            return jsonify(format_error_response("REQUEST_TOO_LARGE", size_error)), 413


@tree_of_thought_bp.route('/explore', methods=['POST'])
def explore_problem():
    """
    Multi-Approach Problem Exploration using Tree-of-Thought
    ---
    tags:
      - Tree-of-Thought
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - problem
          properties:
            problem:
              type: string
              description: Complex problem to explore with multiple approaches
              example: "How can we reduce plastic waste in our city?"
            max_approaches:
              type: integer
              description: Maximum number of approaches to explore (1-5)
              example: 3
              default: 3
              minimum: 1
              maximum: 5
    responses:
      200:
        description: Multiple solution approaches with best selection
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                technique:
                  type: string
                  example: "Tree-of-Thought"
                task:
                  type: string
                  example: "multi_approach_exploration"
                input:
                  type: string
                output:
                  type: object
                  properties:
                    explored_approaches:
                      type: array
                      items:
                        type: object
                        properties:
                          approach_number:
                            type: integer
                          approach_name:
                            type: string
                          solution:
                            type: string
                    best_approach:
                      type: object
                      properties:
                        evaluation:
                          type: string
                        selection_criteria:
                          type: array
                          items:
                            type: string
                    total_approaches:
                      type: integer
                metadata:
                  type: object
      400:
        description: Bad request - Invalid input
      429:
        description: Rate limit exceeded
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        
        # Validate request data
        validation_errors = validate_tree_of_thought_explore(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Set default max_approaches if not provided
        max_approaches = data.get('max_approaches', 3)
        
        # Run tree-of-thought exploration (async)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                service.tree_of_thought_explore(data['problem'], max_approaches)
            )
        finally:
            loop.close()
        
        logger.info(f"Tree-of-thought exploration completed for: {data['problem'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Tree-of-thought exploration failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("TREE_OF_THOUGHT_FAILED", str(e))), 500


@tree_of_thought_bp.route('/info', methods=['GET'])
def tree_of_thought_info():
    """Get information about tree-of-thought endpoints"""
    info_data = {
        "technique": "Tree-of-Thought",
        "description": "Explore multiple reasoning paths simultaneously and select the best approach",
        "endpoints": {
            "explore": {
                "method": "POST",
                "description": "Explore multiple solution approaches for complex problems",
                "required_fields": ["problem"],
                "optional_fields": ["max_approaches"],
                "example": {
                    "problem": "How can we reduce plastic waste in our city?",
                    "max_approaches": 3
                }
            }
        },
        "features": [
            "Multiple approach exploration",
            "Parallel reasoning paths",
            "Best approach selection",
            "Comprehensive solution analysis"
        ],
        "parameters": {
            "max_approaches": {
                "description": "Maximum number of approaches to explore",
                "type": "integer",
                "default": 3,
                "range": "1-5"
            }
        }
    }
    
    return jsonify(format_technique_response({
        "technique": "Tree-of-Thought",
        "task": "info",
        "input": "endpoint_information",
        "output": info_data,
        "metadata": {"processing_time": 0.001, "model": "info"}
    }))


# Error handlers for this blueprint
@tree_of_thought_bp.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify(format_error_response("BAD_REQUEST", "Invalid request data")), 400


@tree_of_thought_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify(format_error_response("METHOD_NOT_ALLOWED", "Method not allowed for this endpoint")), 405


@tree_of_thought_bp.errorhandler(413)
def request_too_large(error):
    """Handle request too large errors"""
    return jsonify(format_error_response("REQUEST_TOO_LARGE", "Request payload too large")), 413