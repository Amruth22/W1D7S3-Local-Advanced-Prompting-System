"""
Meta-Prompting API Endpoints
Flask blueprint for meta-prompting optimization techniques
"""

import logging
from flask import Blueprint, request, jsonify
from core.prompting_service import get_prompting_service
from utils.response_formatter import format_technique_response, format_error_response, format_validation_error
from utils.validators import (
    validate_meta_prompting_optimize,
    validate_meta_prompting_analyze,
    validate_json_content_type,
    validate_request_size
)

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
meta_prompting_bp = Blueprint('meta_prompting', __name__)


@meta_prompting_bp.before_request
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


@meta_prompting_bp.route('/optimize', methods=['POST'])
def optimize_prompt():
    """
    Prompt Optimization using Meta-Prompting
    ---
    tags:
      - Meta-Prompting
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - task
            - current_prompt
          properties:
            task:
              type: string
              description: Description of the task
              example: "Classify customer feedback"
            current_prompt:
              type: string
              description: Current prompt to optimize
              example: "Is this feedback positive or negative: {text}"
    responses:
      200:
        description: Optimized prompt with improvements
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
                  example: "Meta-Prompting"
                task:
                  type: string
                  example: "prompt_optimization"
                input:
                  type: object
                  properties:
                    task:
                      type: string
                    current_prompt:
                      type: string
                output:
                  type: string
                  description: Optimized prompt with explanations
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
        validation_errors = validate_meta_prompting_optimize(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Optimize prompt
        result = service.meta_prompt_optimization(data['task'], data['current_prompt'])
        
        logger.info(f"Meta-prompt optimization completed for task: {data['task'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Meta-prompt optimization failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("PROMPT_OPTIMIZATION_FAILED", str(e))), 500


@meta_prompting_bp.route('/analyze', methods=['POST'])
def analyze_task():
    """
    Task Analysis using Meta-Prompting
    ---
    tags:
      - Meta-Prompting
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - task
          properties:
            task:
              type: string
              description: Task to analyze for optimal prompting approach
              example: "Create a comprehensive marketing strategy for a new product"
    responses:
      200:
        description: Task analysis with prompting recommendations
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
                  example: "Meta-Prompting"
                task:
                  type: string
                  example: "task_analysis"
                input:
                  type: string
                output:
                  type: string
                  description: Analysis with prompting recommendations
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
        validation_errors = validate_meta_prompting_analyze(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Analyze task
        result = service.meta_task_analysis(data['task'])
        
        logger.info(f"Meta-task analysis completed for: {data['task'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Meta-task analysis failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("TASK_ANALYSIS_FAILED", str(e))), 500


@meta_prompting_bp.route('/info', methods=['GET'])
def meta_prompting_info():
    """Get information about meta-prompting endpoints"""
    info_data = {
        "technique": "Meta-Prompting",
        "description": "Self-improving prompts that optimize themselves for better performance",
        "endpoints": {
            "optimize": {
                "method": "POST",
                "description": "Optimize existing prompts for better performance",
                "required_fields": ["task", "current_prompt"],
                "example": {
                    "task": "Classify customer feedback",
                    "current_prompt": "Is this feedback positive or negative: {text}"
                }
            },
            "analyze": {
                "method": "POST",
                "description": "Analyze tasks to determine optimal prompting approach",
                "required_fields": ["task"],
                "example": {
                    "task": "Create a comprehensive marketing strategy for a new product"
                }
            }
        },
        "features": [
            "Prompt optimization",
            "Task analysis",
            "Self-improving prompts",
            "Performance enhancement"
        ],
        "use_cases": [
            "Improving existing prompts",
            "Analyzing new tasks",
            "Optimizing prompt performance",
            "Adapting prompts to specific domains"
        ],
        "benefits": [
            "Better prompt effectiveness",
            "Reduced trial and error",
            "Domain-specific optimization",
            "Continuous improvement"
        ]
    }
    
    return jsonify(format_technique_response({
        "technique": "Meta-Prompting",
        "task": "info",
        "input": "endpoint_information",
        "output": info_data,
        "metadata": {"processing_time": 0.001, "model": "info"}
    }))


# Error handlers for this blueprint
@meta_prompting_bp.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify(format_error_response("BAD_REQUEST", "Invalid request data")), 400


@meta_prompting_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify(format_error_response("METHOD_NOT_ALLOWED", "Method not allowed for this endpoint")), 405


@meta_prompting_bp.errorhandler(413)
def request_too_large(error):
    """Handle request too large errors"""
    return jsonify(format_error_response("REQUEST_TOO_LARGE", "Request payload too large")), 413