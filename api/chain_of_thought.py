"""
Chain-of-Thought API Endpoints
Flask blueprint for chain-of-thought reasoning techniques
"""

import logging
from flask import Blueprint, request, jsonify
from core.prompting_service import get_prompting_service
from utils.response_formatter import format_technique_response, format_error_response, format_validation_error
from utils.validators import (
    validate_chain_of_thought_math,
    validate_chain_of_thought_logic,
    validate_chain_of_thought_analysis,
    validate_json_content_type,
    validate_request_size
)

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
chain_of_thought_bp = Blueprint('chain_of_thought', __name__)


@chain_of_thought_bp.before_request
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


@chain_of_thought_bp.route('/math', methods=['POST'])
def math_reasoning():
    """
    Math Reasoning using Chain-of-Thought
    ---
    tags:
      - Chain-of-Thought
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
              description: Math problem requiring step-by-step reasoning
              example: "A car travels 60 mph for 2.5 hours. How far does it travel?"
    responses:
      200:
        description: Step-by-step math solution
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
                  example: "Chain-of-Thought"
                task:
                  type: string
                  example: "math_reasoning"
                input:
                  type: string
                output:
                  type: string
                  example: "Step 1: Identify the given information...\nStep 2: Apply the formula...\nStep 3: Calculate the result..."
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
        validation_errors = validate_chain_of_thought_math(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Solve math problem with reasoning
        result = service.chain_of_thought_math_solver(data['problem'])
        
        logger.info(f"Chain-of-thought math reasoning completed for: {data['problem'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Chain-of-thought math reasoning failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("MATH_REASONING_FAILED", str(e))), 500


@chain_of_thought_bp.route('/logic', methods=['POST'])
def logical_reasoning():
    """
    Logical Reasoning using Chain-of-Thought
    ---
    tags:
      - Chain-of-Thought
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
              description: Logical problem requiring step-by-step analysis
              example: "All birds can fly. Penguins are birds. Can penguins fly?"
    responses:
      200:
        description: Step-by-step logical analysis
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
                  example: "Chain-of-Thought"
                task:
                  type: string
                  example: "logical_reasoning"
                input:
                  type: string
                output:
                  type: string
                  example: "Let me analyze this step by step...\n1. Premise 1: All birds can fly\n2. Premise 2: Penguins are birds\n3. Logical conclusion..."
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
        validation_errors = validate_chain_of_thought_logic(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Solve logical problem with reasoning
        result = service.chain_of_thought_logical_reasoning(data['problem'])
        
        logger.info(f"Chain-of-thought logical reasoning completed for: {data['problem'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Chain-of-thought logical reasoning failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("LOGICAL_REASONING_FAILED", str(e))), 500


@chain_of_thought_bp.route('/analysis', methods=['POST'])
def complex_analysis():
    """
    Complex Analysis using Chain-of-Thought
    ---
    tags:
      - Chain-of-Thought
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
              description: Complex problem requiring detailed analysis
              example: "What are the potential impacts of AI on employment?"
    responses:
      200:
        description: Detailed step-by-step analysis
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
                  example: "Chain-of-Thought"
                task:
                  type: string
                  example: "complex_analysis"
                input:
                  type: string
                output:
                  type: string
                  example: "Let me break down this complex issue...\n1. Current state analysis...\n2. Potential positive impacts...\n3. Potential negative impacts..."
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
        validation_errors = validate_chain_of_thought_analysis(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Perform complex analysis with reasoning
        result = service.chain_of_thought_complex_analysis(data['problem'])
        
        logger.info(f"Chain-of-thought complex analysis completed for: {data['problem'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Chain-of-thought complex analysis failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("COMPLEX_ANALYSIS_FAILED", str(e))), 500


@chain_of_thought_bp.route('/info', methods=['GET'])
def chain_of_thought_info():
    """Get information about chain-of-thought endpoints"""
    info_data = {
        "technique": "Chain-of-Thought",
        "description": "Step-by-step reasoning for complex problem solving",
        "endpoints": {
            "math": {
                "method": "POST",
                "description": "Solve math problems with step-by-step reasoning",
                "required_fields": ["problem"],
                "example": {
                    "problem": "A car travels 60 mph for 2.5 hours. How far does it travel?"
                }
            },
            "logic": {
                "method": "POST",
                "description": "Solve logical problems with systematic reasoning",
                "required_fields": ["problem"],
                "example": {
                    "problem": "All birds can fly. Penguins are birds. Can penguins fly? Explain the logical issue."
                }
            },
            "analysis": {
                "method": "POST",
                "description": "Analyze complex problems with detailed reasoning",
                "required_fields": ["problem"],
                "example": {
                    "problem": "What are the potential impacts of artificial intelligence on employment?"
                }
            }
        },
        "features": [
            "Step-by-step reasoning process",
            "Detailed problem breakdown",
            "Logical deduction and analysis",
            "Comprehensive solution development"
        ]
    }
    
    return jsonify(format_technique_response({
        "technique": "Chain-of-Thought",
        "task": "info",
        "input": "endpoint_information",
        "output": info_data,
        "metadata": {"processing_time": 0.001, "model": "info"}
    }))


# Error handlers for this blueprint
@chain_of_thought_bp.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify(format_error_response("BAD_REQUEST", "Invalid request data")), 400


@chain_of_thought_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify(format_error_response("METHOD_NOT_ALLOWED", "Method not allowed for this endpoint")), 405


@chain_of_thought_bp.errorhandler(413)
def request_too_large(error):
    """Handle request too large errors"""
    return jsonify(format_error_response("REQUEST_TOO_LARGE", "Request payload too large")), 413