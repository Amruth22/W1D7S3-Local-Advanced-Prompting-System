"""
Few-shot Learning API Endpoints
Flask blueprint for few-shot learning techniques
"""

import logging
from flask import Blueprint, request, jsonify
from core.prompting_service import get_prompting_service
from utils.response_formatter import format_technique_response, format_error_response, format_validation_error
from utils.validators import (
    validate_few_shot_sentiment,
    validate_few_shot_math,
    validate_few_shot_ner,
    validate_few_shot_classification,
    validate_json_content_type,
    validate_request_size
)

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
few_shot_bp = Blueprint('few_shot', __name__)


@few_shot_bp.before_request
def validate_request():
    """Validate request before processing"""
    # Check content type
    content_type_error = validate_json_content_type(request)
    if content_type_error:
        return jsonify(format_error_response("INVALID_CONTENT_TYPE", content_type_error)), 400
    
    # Check request size
    size_error = validate_request_size(request, max_size_mb=1)
    if size_error:
        return jsonify(format_error_response("REQUEST_TOO_LARGE", size_error)), 413


@few_shot_bp.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    """
    Perform sentiment analysis using few-shot learning
    
    Expected JSON payload:
    {
        "text": "Text to analyze for sentiment"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request data
        validation_errors = validate_few_shot_sentiment(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Perform sentiment analysis
        result = service.few_shot_sentiment_analysis(data['text'])
        
        logger.info(f"Sentiment analysis completed for text: {data['text'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("SENTIMENT_ANALYSIS_FAILED", str(e))), 500


@few_shot_bp.route('/math', methods=['POST'])
def math_solver():
    """
    Solve math problems using few-shot learning
    
    Expected JSON payload:
    {
        "problem": "Math problem to solve"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request data
        validation_errors = validate_few_shot_math(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Solve math problem
        result = service.few_shot_math_solver(data['problem'])
        
        logger.info(f"Math problem solved: {data['problem'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Math solving failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("MATH_SOLVING_FAILED", str(e))), 500


@few_shot_bp.route('/ner', methods=['POST'])
def named_entity_recognition():
    """
    Extract named entities using few-shot learning
    
    Expected JSON payload:
    {
        "text": "Text to extract entities from"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request data
        validation_errors = validate_few_shot_ner(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Extract named entities
        result = service.few_shot_named_entity_recognition(data['text'])
        
        logger.info(f"NER completed for text: {data['text'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"NER failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("NER_FAILED", str(e))), 500


@few_shot_bp.route('/classification', methods=['POST'])
def text_classification():
    """
    Classify text using few-shot learning
    
    Expected JSON payload:
    {
        "text": "Text to classify"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request data
        validation_errors = validate_few_shot_classification(data)
        if validation_errors:
            return jsonify(format_validation_error(validation_errors)), 400
        
        # Get prompting service
        service = get_prompting_service()
        
        # Classify text
        result = service.few_shot_text_classification(data['text'])
        
        logger.info(f"Text classification completed for: {data['text'][:50]}...")
        
        return jsonify(format_technique_response(result))
        
    except Exception as e:
        logger.error(f"Text classification failed: {str(e)}")
        
        # Handle rate limiting
        if "rate limit" in str(e).lower() or "429" in str(e):
            return jsonify(format_error_response(
                "RATE_LIMIT_EXCEEDED", 
                "Rate limit exceeded. Please wait before making another request."
            )), 429
        
        return jsonify(format_error_response("TEXT_CLASSIFICATION_FAILED", str(e))), 500


@few_shot_bp.route('/info', methods=['GET'])
def few_shot_info():
    """Get information about few-shot learning endpoints"""
    info_data = {
        "technique": "Few-shot Learning",
        "description": "Learn from minimal examples to perform new tasks",
        "endpoints": {
            "sentiment": {
                "method": "POST",
                "description": "Analyze sentiment of text",
                "required_fields": ["text"],
                "example": {"text": "This product is amazing!"}
            },
            "math": {
                "method": "POST", 
                "description": "Solve math word problems",
                "required_fields": ["problem"],
                "example": {"problem": "If John has 15 apples and gives away 7, how many does he have left?"}
            },
            "ner": {
                "method": "POST",
                "description": "Extract named entities from text",
                "required_fields": ["text"],
                "example": {"text": "Apple Inc. was founded by Steve Jobs in California."}
            },
            "classification": {
                "method": "POST",
                "description": "Classify text into categories",
                "required_fields": ["text"],
                "example": {"text": "How do I reset my password?"}
            }
        }
    }
    
    return jsonify(format_technique_response({
        "technique": "Few-shot Learning",
        "task": "info",
        "input": "endpoint_information",
        "output": info_data,
        "metadata": {"processing_time": 0.001, "model": "info"}
    }))


# Error handlers for this blueprint
@few_shot_bp.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify(format_error_response("BAD_REQUEST", "Invalid request data")), 400


@few_shot_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify(format_error_response("METHOD_NOT_ALLOWED", "Method not allowed for this endpoint")), 405


@few_shot_bp.errorhandler(413)
def request_too_large(error):
    """Handle request too large errors"""
    return jsonify(format_error_response("REQUEST_TOO_LARGE", "Request payload too large")), 413