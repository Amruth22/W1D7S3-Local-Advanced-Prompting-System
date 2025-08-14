"""
Response Formatter Utility
Standardizes API response format across all endpoints
"""

from datetime import datetime
from typing import Any, Dict, Optional


def format_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
    """
    Format successful API response
    
    Args:
        data: Response data
        message: Optional success message
        
    Returns:
        Formatted success response dictionary
    """
    response = {
        "success": True,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if message:
        response["message"] = message
    
    return response


def format_error_response(
    error_code: str, 
    error_message: str, 
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format error API response
    
    Args:
        error_code: Error code identifier
        error_message: Human-readable error message
        details: Optional additional error details
        
    Returns:
        Formatted error response dictionary
    """
    response = {
        "success": False,
        "error": {
            "code": error_code,
            "message": error_message
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if details:
        response["error"]["details"] = details
    
    return response


def format_technique_response(
    technique_result: Dict[str, Any], 
    success_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format response for prompting technique results
    
    Args:
        technique_result: Result from prompting service
        success_message: Optional success message
        
    Returns:
        Formatted technique response
    """
    # Extract metadata for response headers
    metadata = technique_result.get("metadata", {})
    
    formatted_data = {
        "technique": technique_result.get("technique"),
        "task": technique_result.get("task"),
        "input": technique_result.get("input"),
        "output": technique_result.get("output"),
        "processing_time": metadata.get("processing_time"),
        "model": metadata.get("model"),
        "additional_info": {
            k: v for k, v in metadata.items() 
            if k not in ["processing_time", "model"]
        }
    }
    
    return format_success_response(
        formatted_data, 
        success_message or f"{technique_result.get('technique')} completed successfully"
    )


def format_validation_error(validation_errors: Dict[str, str]) -> Dict[str, Any]:
    """
    Format validation error response
    
    Args:
        validation_errors: Dictionary of field validation errors
        
    Returns:
        Formatted validation error response
    """
    return format_error_response(
        "VALIDATION_ERROR",
        "Request validation failed",
        {"validation_errors": validation_errors}
    )


def format_rate_limit_error(retry_after: Optional[int] = None) -> Dict[str, Any]:
    """
    Format rate limit error response
    
    Args:
        retry_after: Seconds to wait before retrying
        
    Returns:
        Formatted rate limit error response
    """
    details = {}
    if retry_after:
        details["retry_after"] = retry_after
        details["message"] = f"Please wait {retry_after} seconds before making another request"
    
    return format_error_response(
        "RATE_LIMIT_EXCEEDED",
        "Too many requests. Please wait before trying again.",
        details
    )


def format_api_error(exception: Exception) -> Dict[str, Any]:
    """
    Format API error from exception
    
    Args:
        exception: Exception that occurred
        
    Returns:
        Formatted API error response
    """
    error_message = str(exception)
    
    # Check for specific error types
    if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
        return format_rate_limit_error(60)  # Suggest 60 second wait
    elif "INVALID" in error_message.upper():
        return format_error_response("INVALID_INPUT", error_message)
    elif "NOT_FOUND" in error_message.upper():
        return format_error_response("NOT_FOUND", error_message)
    else:
        return format_error_response("API_ERROR", error_message)


def add_response_metadata(
    response: Dict[str, Any], 
    request_id: Optional[str] = None,
    api_version: str = "v1"
) -> Dict[str, Any]:
    """
    Add metadata to response
    
    Args:
        response: Response dictionary
        request_id: Optional request ID for tracking
        api_version: API version
        
    Returns:
        Response with added metadata
    """
    if "metadata" not in response:
        response["metadata"] = {}
    
    response["metadata"]["api_version"] = api_version
    
    if request_id:
        response["metadata"]["request_id"] = request_id
    
    return response


def format_health_response(
    status: str, 
    services: Dict[str, bool], 
    additional_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format health check response
    
    Args:
        status: Overall health status
        services: Dictionary of service statuses
        additional_info: Optional additional health information
        
    Returns:
        Formatted health response
    """
    health_data = {
        "status": status,
        "services": services,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if additional_info:
        health_data.update(additional_info)
    
    return format_success_response(health_data)


def format_async_response(
    task_id: str, 
    status: str = "processing",
    estimated_completion: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format response for asynchronous operations
    
    Args:
        task_id: Unique task identifier
        status: Current task status
        estimated_completion: Estimated completion time
        
    Returns:
        Formatted async response
    """
    async_data = {
        "task_id": task_id,
        "status": status,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    if estimated_completion:
        async_data["estimated_completion"] = estimated_completion
    
    return format_success_response(
        async_data,
        f"Task {task_id} started successfully"
    )