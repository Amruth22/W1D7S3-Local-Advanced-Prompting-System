"""
Comprehensive API Unit Tests
Tests all Flask API endpoints with automatic server management and mocked responses
"""

import pytest
import requests
import json
import time
from unittest.mock import patch, MagicMock


class TestAPIHealth:
    """Test API health and basic functionality"""
    
    def test_health_endpoint(self, live_server, api_headers):
        """Test health check endpoint"""
        response = requests.get(f"{live_server}/api/health", headers=api_headers)
        
        assert response.status_code in [200, 503]  # 503 is acceptable if Gemini is mocked
        
        data = response.json()
        assert "success" in data
        assert "data" in data
        
        health_data = data["data"]
        assert "status" in health_data
        assert "services" in health_data
        assert "flask_app" in health_data["services"]
        assert health_data["services"]["flask_app"] is True
    
    def test_api_info_endpoint(self, live_server, api_headers):
        """Test API info endpoint"""
        response = requests.get(f"{live_server}/api/info", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        
        info_data = data["data"]
        assert "api_name" in info_data
        assert "version" in info_data
        assert "endpoints" in info_data
        assert "few_shot" in info_data["endpoints"]
        assert "chain_of_thought" in info_data["endpoints"]
    
    def test_root_endpoint(self, live_server, api_headers):
        """Test root endpoint"""
        response = requests.get(f"{live_server}/", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "message" in data["data"]
        assert "Welcome" in data["data"]["message"]


class TestFewShotEndpoints:
    """Test few-shot learning endpoints"""
    
    def test_sentiment_analysis_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful sentiment analysis"""
        request_data = sample_requests["few_shot_requests"]["sentiment"]
        
        response = requests.post(
            f"{live_server}/api/v1/few-shot/sentiment",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Few-shot Learning")
        
        # Check specific fields
        response_data = data["data"]
        assert response_data["task"] == "sentiment_analysis"
        assert response_data["input"] == request_data["text"]
        assert isinstance(response_data["output"], str)
        assert len(response_data["output"]) > 0
    
    def test_sentiment_analysis_validation_error(self, live_server, api_headers, api_helper):
        """Test sentiment analysis with validation error"""
        # Missing required field
        request_data = {}
        
        response = requests.post(
            f"{live_server}/api/v1/few-shot/sentiment",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 400
        
        data = response.json()
        api_helper.assert_validation_error(data)
    
    def test_math_solver_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful math problem solving"""
        request_data = sample_requests["few_shot_requests"]["math"]
        
        response = requests.post(
            f"{live_server}/api/v1/few-shot/math",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Few-shot Learning")
        
        response_data = data["data"]
        assert response_data["task"] == "math_solving"
        assert response_data["input"] == request_data["problem"]
    
    def test_ner_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful named entity recognition"""
        request_data = sample_requests["few_shot_requests"]["ner"]
        
        response = requests.post(
            f"{live_server}/api/v1/few-shot/ner",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Few-shot Learning")
        
        response_data = data["data"]
        assert response_data["task"] == "named_entity_recognition"
    
    def test_classification_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful text classification"""
        request_data = sample_requests["few_shot_requests"]["classification"]
        
        response = requests.post(
            f"{live_server}/api/v1/few-shot/classification",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Few-shot Learning")
        
        response_data = data["data"]
        assert response_data["task"] == "text_classification"
    
    def test_few_shot_info(self, live_server, api_headers, api_helper):
        """Test few-shot info endpoint"""
        response = requests.get(f"{live_server}/api/v1/few-shot/info", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_success_response(data)
        
        info_data = data["data"]["output"]
        assert "technique" in info_data
        assert info_data["technique"] == "Few-shot Learning"
        assert "endpoints" in info_data


class TestChainOfThoughtEndpoints:
    """Test chain-of-thought reasoning endpoints"""
    
    def test_math_reasoning_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful math reasoning"""
        request_data = sample_requests["chain_of_thought_requests"]["math"]
        
        response = requests.post(
            f"{live_server}/api/v1/chain-of-thought/math",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Chain-of-Thought")
        
        response_data = data["data"]
        assert response_data["task"] == "math_reasoning"
        assert "step" in response_data["output"].lower() or "solution" in response_data["output"].lower()
    
    def test_logical_reasoning_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful logical reasoning"""
        request_data = sample_requests["chain_of_thought_requests"]["logic"]
        
        response = requests.post(
            f"{live_server}/api/v1/chain-of-thought/logic",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Chain-of-Thought")
        
        response_data = data["data"]
        assert response_data["task"] == "logical_reasoning"
    
    def test_complex_analysis_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful complex analysis"""
        request_data = sample_requests["chain_of_thought_requests"]["analysis"]
        
        response = requests.post(
            f"{live_server}/api/v1/chain-of-thought/analysis",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Chain-of-Thought")
        
        response_data = data["data"]
        assert response_data["task"] == "complex_analysis"
    
    def test_chain_of_thought_info(self, live_server, api_headers, api_helper):
        """Test chain-of-thought info endpoint"""
        response = requests.get(f"{live_server}/api/v1/chain-of-thought/info", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_success_response(data)
        
        info_data = data["data"]["output"]
        assert info_data["technique"] == "Chain-of-Thought"


@pytest.mark.slow
class TestTreeOfThoughtEndpoints:
    """Test tree-of-thought exploration endpoints"""
    
    def test_explore_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful tree-of-thought exploration"""
        request_data = sample_requests["tree_of_thought_requests"]["explore"]
        
        response = requests.post(
            f"{live_server}/api/v1/tree-of-thought/explore",
            headers=api_headers,
            json=request_data,
            timeout=30  # Longer timeout for async operations
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Tree-of-Thought")
        
        response_data = data["data"]
        assert response_data["task"] == "multi_approach_exploration"
        assert "explored_approaches" in response_data["output"]
        assert "best_approach" in response_data["output"]
    
    def test_explore_with_custom_approaches(self, live_server, api_headers, api_helper):
        """Test tree-of-thought with custom number of approaches"""
        request_data = {
            "problem": "How to improve team productivity?",
            "max_approaches": 2
        }
        
        response = requests.post(
            f"{live_server}/api/v1/tree-of-thought/explore",
            headers=api_headers,
            json=request_data,
            timeout=30
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Tree-of-Thought")
    
    def test_tree_of_thought_info(self, live_server, api_headers, api_helper):
        """Test tree-of-thought info endpoint"""
        response = requests.get(f"{live_server}/api/v1/tree-of-thought/info", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_success_response(data)
        
        info_data = data["data"]["output"]
        assert info_data["technique"] == "Tree-of-Thought"


@pytest.mark.slow
class TestSelfConsistencyEndpoints:
    """Test self-consistency validation endpoints"""
    
    def test_validate_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful self-consistency validation"""
        request_data = sample_requests["self_consistency_requests"]["validate"]
        
        response = requests.post(
            f"{live_server}/api/v1/self-consistency/validate",
            headers=api_headers,
            json=request_data,
            timeout=30  # Longer timeout for multiple sampling
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Self-Consistency")
        
        response_data = data["data"]
        assert response_data["task"] == "consistency_validation"
        assert "all_responses" in response_data["output"]
        assert "final_answer" in response_data["output"]
        assert "num_samples" in response_data["output"]
    
    def test_validate_with_custom_samples(self, live_server, api_headers, api_helper):
        """Test self-consistency with custom number of samples"""
        request_data = {
            "question": "What is the capital of France?",
            "num_samples": 2
        }
        
        response = requests.post(
            f"{live_server}/api/v1/self-consistency/validate",
            headers=api_headers,
            json=request_data,
            timeout=30
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Self-Consistency")
    
    def test_self_consistency_info(self, live_server, api_headers, api_helper):
        """Test self-consistency info endpoint"""
        response = requests.get(f"{live_server}/api/v1/self-consistency/info", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_success_response(data)
        
        info_data = data["data"]["output"]
        assert info_data["technique"] == "Self-Consistency"


class TestMetaPromptingEndpoints:
    """Test meta-prompting optimization endpoints"""
    
    def test_optimize_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful prompt optimization"""
        request_data = sample_requests["meta_prompting_requests"]["optimize"]
        
        response = requests.post(
            f"{live_server}/api/v1/meta-prompting/optimize",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Meta-Prompting")
        
        response_data = data["data"]
        assert response_data["task"] == "prompt_optimization"
        assert "task" in response_data["input"]
        assert "current_prompt" in response_data["input"]
    
    def test_analyze_success(self, live_server, api_headers, sample_requests, api_helper):
        """Test successful task analysis"""
        request_data = sample_requests["meta_prompting_requests"]["analyze"]
        
        response = requests.post(
            f"{live_server}/api/v1/meta-prompting/analyze",
            headers=api_headers,
            json=request_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_technique_response(data, "Meta-Prompting")
        
        response_data = data["data"]
        assert response_data["task"] == "task_analysis"
    
    def test_meta_prompting_info(self, live_server, api_headers, api_helper):
        """Test meta-prompting info endpoint"""
        response = requests.get(f"{live_server}/api/v1/meta-prompting/info", headers=api_headers)
        
        assert response.status_code == 200
        
        data = response.json()
        api_helper.assert_success_response(data)
        
        info_data = data["data"]["output"]
        assert info_data["technique"] == "Meta-Prompting"


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_content_type(self, live_server):
        """Test invalid content type handling"""
        response = requests.post(
            f"{live_server}/api/v1/few-shot/sentiment",
            headers={'Content-Type': 'text/plain'},
            data="invalid data"
        )
        
        assert response.status_code == 400
        
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "INVALID_CONTENT_TYPE"
    
    def test_missing_json_data(self, live_server, api_headers):
        """Test missing JSON data"""
        response = requests.post(
            f"{live_server}/api/v1/few-shot/sentiment",
            headers=api_headers
        )
        
        assert response.status_code == 400
    
    def test_invalid_endpoint(self, live_server, api_headers):
        """Test invalid endpoint"""
        response = requests.get(f"{live_server}/api/v1/invalid-endpoint", headers=api_headers)
        
        assert response.status_code == 404
        
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "NOT_FOUND"
    
    def test_method_not_allowed(self, live_server, api_headers):
        """Test method not allowed"""
        response = requests.get(f"{live_server}/api/v1/few-shot/sentiment", headers=api_headers)
        
        assert response.status_code == 405
        
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "METHOD_NOT_ALLOWED"


class TestPerformance:
    """Test API performance with mocked responses"""
    
    def test_response_time(self, live_server, api_headers, sample_requests):
        """Test that mocked responses are fast"""
        request_data = sample_requests["few_shot_requests"]["sentiment"]
        
        start_time = time.time()
        
        response = requests.post(
            f"{live_server}/api/v1/few-shot/sentiment",
            headers=api_headers,
            json=request_data
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0  # Should be fast with mocks
        
        data = response.json()
        assert "processing_time" in data["data"]
    
    def test_multiple_requests(self, live_server, api_headers, sample_requests):
        """Test multiple requests performance"""
        request_data = sample_requests["few_shot_requests"]["sentiment"]
        
        start_time = time.time()
        
        # Make 5 requests
        responses = []
        for _ in range(5):
            response = requests.post(
                f"{live_server}/api/v1/few-shot/sentiment",
                headers=api_headers,
                json=request_data
            )
            responses.append(response)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Should be fast with mocks
        assert total_time < 5.0
        
        print(f"5 requests completed in {total_time:.2f} seconds")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])