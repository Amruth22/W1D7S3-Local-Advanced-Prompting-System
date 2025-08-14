"""
Request Validators
Validates incoming API requests and data
"""

from typing import Dict, Any, List, Optional, Union
import re


class ValidationError(Exception):
    """Custom validation error exception"""
    
    def __init__(self, errors: Dict[str, str]):
        self.errors = errors
        super().__init__(f"Validation failed: {errors}")


def validate_request_data(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate request data against schema
    
    Args:
        data: Request data to validate
        schema: Validation schema
        
    Returns:
        Dictionary of validation errors (empty if valid)
    """
    errors = {}
    
    # Check required fields
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in data or data[field] is None:
            errors[field] = f"Field '{field}' is required"
        elif isinstance(data[field], str) and not data[field].strip():
            errors[field] = f"Field '{field}' cannot be empty"
    
    # Check field types and constraints
    field_rules = schema.get("fields", {})
    for field, rules in field_rules.items():
        if field in data and data[field] is not None:
            field_errors = _validate_field(field, data[field], rules)
            if field_errors:
                errors[field] = field_errors
    
    return errors


def _validate_field(field_name: str, value: Any, rules: Dict[str, Any]) -> Optional[str]:
    """
    Validate a single field against its rules
    
    Args:
        field_name: Name of the field
        value: Field value
        rules: Validation rules for the field
        
    Returns:
        Error message if validation fails, None if valid
    """
    # Type validation
    expected_type = rules.get("type")
    if expected_type and not isinstance(value, expected_type):
        return f"Field '{field_name}' must be of type {expected_type.__name__}"
    
    # String validations
    if isinstance(value, str):
        # Length validation
        min_length = rules.get("min_length")
        if min_length and len(value) < min_length:
            return f"Field '{field_name}' must be at least {min_length} characters long"
        
        max_length = rules.get("max_length")
        if max_length and len(value) > max_length:
            return f"Field '{field_name}' must be at most {max_length} characters long"
        
        # Pattern validation
        pattern = rules.get("pattern")
        if pattern and not re.match(pattern, value):
            return f"Field '{field_name}' format is invalid"
        
        # Allowed values
        allowed_values = rules.get("allowed_values")
        if allowed_values and value not in allowed_values:
            return f"Field '{field_name}' must be one of: {', '.join(allowed_values)}"
    
    # Numeric validations
    if isinstance(value, (int, float)):
        min_value = rules.get("min_value")
        if min_value is not None and value < min_value:
            return f"Field '{field_name}' must be at least {min_value}"
        
        max_value = rules.get("max_value")
        if max_value is not None and value > max_value:
            return f"Field '{field_name}' must be at most {max_value}"
    
    # List validations
    if isinstance(value, list):
        min_items = rules.get("min_items")
        if min_items and len(value) < min_items:
            return f"Field '{field_name}' must have at least {min_items} items"
        
        max_items = rules.get("max_items")
        if max_items and len(value) > max_items:
            return f"Field '{field_name}' must have at most {max_items} items"
    
    return None


# Predefined validation schemas
SCHEMAS = {
    "few_shot_sentiment": {
        "required": ["text"],
        "fields": {
            "text": {
                "type": str,
                "min_length": 1,
                "max_length": 5000
            }
        }
    },
    
    "few_shot_math": {
        "required": ["problem"],
        "fields": {
            "problem": {
                "type": str,
                "min_length": 5,
                "max_length": 2000
            }
        }
    },
    
    "few_shot_ner": {
        "required": ["text"],
        "fields": {
            "text": {
                "type": str,
                "min_length": 1,
                "max_length": 3000
            }
        }
    },
    
    "few_shot_classification": {
        "required": ["text"],
        "fields": {
            "text": {
                "type": str,
                "min_length": 1,
                "max_length": 2000
            }
        }
    },
    
    "chain_of_thought_math": {
        "required": ["problem"],
        "fields": {
            "problem": {
                "type": str,
                "min_length": 5,
                "max_length": 2000
            }
        }
    },
    
    "chain_of_thought_logic": {
        "required": ["problem"],
        "fields": {
            "problem": {
                "type": str,
                "min_length": 10,
                "max_length": 2000
            }
        }
    },
    
    "chain_of_thought_analysis": {
        "required": ["problem"],
        "fields": {
            "problem": {
                "type": str,
                "min_length": 10,
                "max_length": 3000
            }
        }
    },
    
    "tree_of_thought_explore": {
        "required": ["problem"],
        "fields": {
            "problem": {
                "type": str,
                "min_length": 10,
                "max_length": 2000
            },
            "max_approaches": {
                "type": int,
                "min_value": 1,
                "max_value": 5
            }
        }
    },
    
    "self_consistency_validate": {
        "required": ["question"],
        "fields": {
            "question": {
                "type": str,
                "min_length": 5,
                "max_length": 1000
            },
            "num_samples": {
                "type": int,
                "min_value": 2,
                "max_value": 5
            }
        }
    },
    
    "meta_prompting_optimize": {
        "required": ["task", "current_prompt"],
        "fields": {
            "task": {
                "type": str,
                "min_length": 5,
                "max_length": 500
            },
            "current_prompt": {
                "type": str,
                "min_length": 10,
                "max_length": 2000
            }
        }
    },
    
    "meta_prompting_analyze": {
        "required": ["task"],
        "fields": {
            "task": {
                "type": str,
                "min_length": 5,
                "max_length": 1000
            }
        }
    }
}


def validate_few_shot_sentiment(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate few-shot sentiment analysis request"""
    return validate_request_data(data, SCHEMAS["few_shot_sentiment"])


def validate_few_shot_math(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate few-shot math solving request"""
    return validate_request_data(data, SCHEMAS["few_shot_math"])


def validate_few_shot_ner(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate few-shot NER request"""
    return validate_request_data(data, SCHEMAS["few_shot_ner"])


def validate_few_shot_classification(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate few-shot classification request"""
    return validate_request_data(data, SCHEMAS["few_shot_classification"])


def validate_chain_of_thought_math(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate chain-of-thought math request"""
    return validate_request_data(data, SCHEMAS["chain_of_thought_math"])


def validate_chain_of_thought_logic(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate chain-of-thought logic request"""
    return validate_request_data(data, SCHEMAS["chain_of_thought_logic"])


def validate_chain_of_thought_analysis(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate chain-of-thought analysis request"""
    return validate_request_data(data, SCHEMAS["chain_of_thought_analysis"])


def validate_tree_of_thought_explore(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate tree-of-thought exploration request"""
    return validate_request_data(data, SCHEMAS["tree_of_thought_explore"])


def validate_self_consistency_validate(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate self-consistency validation request"""
    return validate_request_data(data, SCHEMAS["self_consistency_validate"])


def validate_meta_prompting_optimize(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate meta-prompting optimization request"""
    return validate_request_data(data, SCHEMAS["meta_prompting_optimize"])


def validate_meta_prompting_analyze(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate meta-prompting analysis request"""
    return validate_request_data(data, SCHEMAS["meta_prompting_analyze"])


def validate_json_content_type(request) -> Optional[str]:
    """
    Validate that request has JSON content type
    
    Args:
        request: Flask request object
        
    Returns:
        Error message if invalid, None if valid
    """
    if not request.is_json:
        return "Request must have Content-Type: application/json"
    return None


def validate_request_size(request, max_size_mb: int = 1) -> Optional[str]:
    """
    Validate request size
    
    Args:
        request: Flask request object
        max_size_mb: Maximum size in MB
        
    Returns:
        Error message if too large, None if valid
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if request.content_length and request.content_length > max_size_bytes:
        return f"Request too large. Maximum size is {max_size_mb}MB"
    
    return None