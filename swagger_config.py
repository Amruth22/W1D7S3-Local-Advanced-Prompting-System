"""
Swagger UI Configuration
Configures Swagger/OpenAPI documentation for the Flask API
"""

from flask_restx import Api, Resource, fields
from flask import Blueprint


def create_swagger_config():
    """Create Swagger configuration"""
    return {
        'title': 'Local Advanced Prompting System API',
        'version': '1.0.0',
        'description': '''
        A comprehensive Flask API for advanced prompting techniques with local deployment capabilities.
        
        ## Features
        - **Few-shot Learning**: Learn from minimal examples
        - **Chain-of-Thought**: Step-by-step reasoning
        - **Tree-of-Thought**: Multiple path exploration  
        - **Self-Consistency**: Multiple sampling validation
        - **Meta-Prompting**: Self-improving prompts
        
        ## Authentication
        No authentication required for this local API.
        
        ## Rate Limits
        - Free tier: 10 requests per minute
        - Consider request spacing for optimal performance
        ''',
        'contact': {
            'name': 'API Support',
            'url': 'https://github.com/Amruth22/Local-Advanced-Prompting-System'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        },
        'doc': '/docs/',
        'base_url': '/api/v1',
        'validate': True,
        'ordered': True
    }


def create_api_models():
    """Create API models for Swagger documentation"""
    
    # Create a blueprint for API documentation
    api_bp = Blueprint('api_docs', __name__)
    api = Api(api_bp, **create_swagger_config())
    
    # Common response models
    error_model = api.model('Error', {
        'success': fields.Boolean(required=True, description='Success status', example=False),
        'error': fields.Nested(api.model('ErrorDetails', {
            'code': fields.String(required=True, description='Error code', example='VALIDATION_ERROR'),
            'message': fields.String(required=True, description='Error message', example='Invalid input data'),
            'details': fields.Raw(description='Additional error details')
        })),
        'timestamp': fields.String(required=True, description='ISO timestamp', example='2024-01-01T12:00:00Z')
    })
    
    success_model = api.model('Success', {
        'success': fields.Boolean(required=True, description='Success status', example=True),
        'data': fields.Raw(required=True, description='Response data'),
        'timestamp': fields.String(required=True, description='ISO timestamp', example='2024-01-01T12:00:00Z'),
        'message': fields.String(description='Optional success message')
    })
    
    # Few-shot Learning Models
    sentiment_request = api.model('SentimentRequest', {
        'text': fields.String(required=True, description='Text to analyze for sentiment', 
                             example='This product is absolutely amazing!')
    })
    
    math_request = api.model('MathRequest', {
        'problem': fields.String(required=True, description='Math problem to solve',
                                example='If a pizza costs $12 and has 8 slices, what does each slice cost?')
    })
    
    ner_request = api.model('NERRequest', {
        'text': fields.String(required=True, description='Text to extract entities from',
                             example='Apple Inc. was founded by Steve Jobs in California.')
    })
    
    classification_request = api.model('ClassificationRequest', {
        'text': fields.String(required=True, description='Text to classify',
                             example='How do I reset my password?')
    })
    
    # Chain-of-Thought Models
    cot_math_request = api.model('CoTMathRequest', {
        'problem': fields.String(required=True, description='Math problem requiring step-by-step reasoning',
                                example='A car travels 60 mph for 2.5 hours. How far does it travel?')
    })
    
    cot_logic_request = api.model('CoTLogicRequest', {
        'problem': fields.String(required=True, description='Logical problem requiring analysis',
                                example='All birds can fly. Penguins are birds. Can penguins fly?')
    })
    
    cot_analysis_request = api.model('CoTAnalysisRequest', {
        'problem': fields.String(required=True, description='Complex problem requiring detailed analysis',
                                example='What are the potential impacts of AI on employment?')
    })
    
    # Tree-of-Thought Models
    tot_explore_request = api.model('ToTExploreRequest', {
        'problem': fields.String(required=True, description='Complex problem to explore with multiple approaches',
                                example='How can we reduce plastic waste in our city?'),
        'max_approaches': fields.Integer(description='Maximum number of approaches to explore (1-5)', 
                                       example=3, default=3)
    })
    
    # Self-Consistency Models
    sc_validate_request = api.model('SCValidateRequest', {
        'question': fields.String(required=True, description='Question to answer with consistency validation',
                                 example='What are the main benefits of renewable energy?'),
        'num_samples': fields.Integer(description='Number of samples for consistency check (2-5)',
                                    example=3, default=3)
    })
    
    # Meta-Prompting Models
    mp_optimize_request = api.model('MPOptimizeRequest', {
        'task': fields.String(required=True, description='Task description',
                             example='Classify customer feedback'),
        'current_prompt': fields.String(required=True, description='Current prompt to optimize',
                                       example='Is this feedback positive or negative: {text}')
    })
    
    mp_analyze_request = api.model('MPAnalyzeRequest', {
        'task': fields.String(required=True, description='Task to analyze for optimal prompting',
                             example='Create a comprehensive marketing strategy')
    })
    
    # Technique Response Model
    technique_response = api.model('TechniqueResponse', {
        'success': fields.Boolean(required=True, description='Success status', example=True),
        'data': fields.Nested(api.model('TechniqueData', {
            'technique': fields.String(required=True, description='Prompting technique used', 
                                     example='Few-shot Learning'),
            'task': fields.String(required=True, description='Specific task performed',
                                 example='sentiment_analysis'),
            'input': fields.Raw(required=True, description='Input data provided'),
            'output': fields.Raw(required=True, description='Generated output'),
            'processing_time': fields.Float(description='Processing time in seconds', example=1.23),
            'model': fields.String(description='AI model used', example='gemini-2.5-flash'),
            'additional_info': fields.Raw(description='Additional metadata')
        })),
        'timestamp': fields.String(required=True, description='ISO timestamp'),
        'message': fields.String(description='Success message')
    })
    
    # Health Response Model
    health_response = api.model('HealthResponse', {
        'success': fields.Boolean(required=True, example=True),
        'data': fields.Nested(api.model('HealthData', {
            'status': fields.String(required=True, description='Overall health status', 
                                   example='healthy'),
            'services': fields.Nested(api.model('ServiceStatus', {
                'flask_app': fields.Boolean(example=True),
                'gemini_api': fields.Boolean(example=True),
                'prompting_service': fields.Boolean(example=True)
            })),
            'model_info': fields.Raw(description='AI model information'),
            'timestamp': fields.String(example='2024-01-01T12:00:00Z')
        })),
        'timestamp': fields.String(required=True)
    })
    
    return {
        'api': api,
        'blueprint': api_bp,
        'models': {
            'error': error_model,
            'success': success_model,
            'technique_response': technique_response,
            'health_response': health_response,
            'sentiment_request': sentiment_request,
            'math_request': math_request,
            'ner_request': ner_request,
            'classification_request': classification_request,
            'cot_math_request': cot_math_request,
            'cot_logic_request': cot_logic_request,
            'cot_analysis_request': cot_analysis_request,
            'tot_explore_request': tot_explore_request,
            'sc_validate_request': sc_validate_request,
            'mp_optimize_request': mp_optimize_request,
            'mp_analyze_request': mp_analyze_request
        }
    }


# HTTP status codes for documentation
HTTP_200_OK = 'Success'
HTTP_400_BAD_REQUEST = 'Bad Request - Invalid input data'
HTTP_404_NOT_FOUND = 'Not Found - Endpoint does not exist'
HTTP_405_METHOD_NOT_ALLOWED = 'Method Not Allowed'
HTTP_413_REQUEST_TOO_LARGE = 'Request Too Large'
HTTP_429_TOO_MANY_REQUESTS = 'Too Many Requests - Rate limit exceeded'
HTTP_500_INTERNAL_ERROR = 'Internal Server Error'
HTTP_503_SERVICE_UNAVAILABLE = 'Service Unavailable'