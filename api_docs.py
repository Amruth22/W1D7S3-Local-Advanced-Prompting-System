"""
API Documentation with Swagger UI
Creates documented API endpoints using Flask-RESTX
"""

from flask import request
from flask_restx import Resource, Namespace
import asyncio
import logging

from core.prompting_service import get_prompting_service
from utils.response_formatter import format_technique_response, format_error_response, format_validation_error
from utils.validators import (
    validate_few_shot_sentiment, validate_few_shot_math, validate_few_shot_ner, validate_few_shot_classification,
    validate_chain_of_thought_math, validate_chain_of_thought_logic, validate_chain_of_thought_analysis,
    validate_tree_of_thought_explore, validate_self_consistency_validate,
    validate_meta_prompting_optimize, validate_meta_prompting_analyze
)
from swagger_config import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS, HTTP_500_INTERNAL_ERROR

logger = logging.getLogger(__name__)


def create_documented_endpoints(api, models):
    """Create all documented API endpoints"""
    
    # Few-shot Learning Namespace
    few_shot_ns = Namespace('few-shot', description='Few-shot Learning Techniques')
    
    @few_shot_ns.route('/sentiment')
    class SentimentAnalysis(Resource):
        @few_shot_ns.expect(models['sentiment_request'])
        @few_shot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @few_shot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @few_shot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @few_shot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Analyze sentiment using few-shot learning"""
            try:
                data = request.get_json()
                validation_errors = validate_few_shot_sentiment(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.few_shot_sentiment_analysis(data['text'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"Sentiment analysis failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("SENTIMENT_ANALYSIS_FAILED", str(e)), 500
    
    @few_shot_ns.route('/math')
    class MathSolver(Resource):
        @few_shot_ns.expect(models['math_request'])
        @few_shot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @few_shot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @few_shot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @few_shot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Solve math problems using few-shot learning"""
            try:
                data = request.get_json()
                validation_errors = validate_few_shot_math(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.few_shot_math_solver(data['problem'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"Math solving failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("MATH_SOLVING_FAILED", str(e)), 500
    
    @few_shot_ns.route('/ner')
    class NamedEntityRecognition(Resource):
        @few_shot_ns.expect(models['ner_request'])
        @few_shot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @few_shot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @few_shot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @few_shot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Extract named entities using few-shot learning"""
            try:
                data = request.get_json()
                validation_errors = validate_few_shot_ner(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.few_shot_named_entity_recognition(data['text'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"NER failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("NER_FAILED", str(e)), 500
    
    @few_shot_ns.route('/classification')
    class TextClassification(Resource):
        @few_shot_ns.expect(models['classification_request'])
        @few_shot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @few_shot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @few_shot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @few_shot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Classify text using few-shot learning"""
            try:
                data = request.get_json()
                validation_errors = validate_few_shot_classification(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.few_shot_text_classification(data['text'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"Text classification failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("TEXT_CLASSIFICATION_FAILED", str(e)), 500
    
    # Chain-of-Thought Namespace
    cot_ns = Namespace('chain-of-thought', description='Chain-of-Thought Reasoning')
    
    @cot_ns.route('/math')
    class ChainOfThoughtMath(Resource):
        @cot_ns.expect(models['cot_math_request'])
        @cot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @cot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @cot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @cot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Solve math problems with step-by-step reasoning"""
            try:
                data = request.get_json()
                validation_errors = validate_chain_of_thought_math(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.chain_of_thought_math_solver(data['problem'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"CoT math reasoning failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("MATH_REASONING_FAILED", str(e)), 500
    
    @cot_ns.route('/logic')
    class ChainOfThoughtLogic(Resource):
        @cot_ns.expect(models['cot_logic_request'])
        @cot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @cot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @cot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @cot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Solve logical problems with systematic reasoning"""
            try:
                data = request.get_json()
                validation_errors = validate_chain_of_thought_logic(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.chain_of_thought_logical_reasoning(data['problem'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"CoT logical reasoning failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("LOGICAL_REASONING_FAILED", str(e)), 500
    
    @cot_ns.route('/analysis')
    class ChainOfThoughtAnalysis(Resource):
        @cot_ns.expect(models['cot_analysis_request'])
        @cot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @cot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @cot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @cot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Analyze complex problems with detailed reasoning"""
            try:
                data = request.get_json()
                validation_errors = validate_chain_of_thought_analysis(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.chain_of_thought_complex_analysis(data['problem'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"CoT complex analysis failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("COMPLEX_ANALYSIS_FAILED", str(e)), 500
    
    # Tree-of-Thought Namespace
    tot_ns = Namespace('tree-of-thought', description='Tree-of-Thought Exploration')
    
    @tot_ns.route('/explore')
    class TreeOfThoughtExplore(Resource):
        @tot_ns.expect(models['tot_explore_request'])
        @tot_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @tot_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @tot_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @tot_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Explore multiple solution approaches"""
            try:
                data = request.get_json()
                validation_errors = validate_tree_of_thought_explore(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                max_approaches = data.get('max_approaches', 3)
                
                # Run async operation
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(
                        service.tree_of_thought_explore(data['problem'], max_approaches)
                    )
                finally:
                    loop.close()
                
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"ToT exploration failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("TREE_OF_THOUGHT_FAILED", str(e)), 500
    
    # Self-Consistency Namespace
    sc_ns = Namespace('self-consistency', description='Self-Consistency Validation')
    
    @sc_ns.route('/validate')
    class SelfConsistencyValidate(Resource):
        @sc_ns.expect(models['sc_validate_request'])
        @sc_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @sc_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @sc_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @sc_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Get consistent answers using multiple sampling"""
            try:
                data = request.get_json()
                validation_errors = validate_self_consistency_validate(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                num_samples = data.get('num_samples', 3)
                
                # Run async operation
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(
                        service.self_consistency_validate(data['question'], num_samples)
                    )
                finally:
                    loop.close()
                
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"Self-consistency validation failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("SELF_CONSISTENCY_FAILED", str(e)), 500
    
    # Meta-Prompting Namespace
    mp_ns = Namespace('meta-prompting', description='Meta-Prompting Optimization')
    
    @mp_ns.route('/optimize')
    class MetaPromptingOptimize(Resource):
        @mp_ns.expect(models['mp_optimize_request'])
        @mp_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @mp_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @mp_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @mp_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Optimize prompts for better performance"""
            try:
                data = request.get_json()
                validation_errors = validate_meta_prompting_optimize(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.meta_prompt_optimization(data['task'], data['current_prompt'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"Meta-prompt optimization failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("PROMPT_OPTIMIZATION_FAILED", str(e)), 500
    
    @mp_ns.route('/analyze')
    class MetaPromptingAnalyze(Resource):
        @mp_ns.expect(models['mp_analyze_request'])
        @mp_ns.marshal_with(models['technique_response'], code=200, description=HTTP_200_OK)
        @mp_ns.response(400, HTTP_400_BAD_REQUEST, models['error'])
        @mp_ns.response(429, HTTP_429_TOO_MANY_REQUESTS, models['error'])
        @mp_ns.response(500, HTTP_500_INTERNAL_ERROR, models['error'])
        def post(self):
            """Analyze tasks for optimal prompting approach"""
            try:
                data = request.get_json()
                validation_errors = validate_meta_prompting_analyze(data)
                if validation_errors:
                    return format_validation_error(validation_errors), 400
                
                service = get_prompting_service()
                result = service.meta_task_analysis(data['task'])
                return format_technique_response(result)
                
            except Exception as e:
                logger.error(f"Meta-task analysis failed: {str(e)}")
                if "rate limit" in str(e).lower() or "429" in str(e):
                    return format_error_response("RATE_LIMIT_EXCEEDED", str(e)), 429
                return format_error_response("TASK_ANALYSIS_FAILED", str(e)), 500
    
    # Add namespaces to API
    api.add_namespace(few_shot_ns)
    api.add_namespace(cot_ns)
    api.add_namespace(tot_ns)
    api.add_namespace(sc_ns)
    api.add_namespace(mp_ns)
    
    return api