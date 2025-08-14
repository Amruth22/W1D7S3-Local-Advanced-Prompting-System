"""
Pytest Configuration and Fixtures
Shared test configuration and fixtures for the Flask API tests
"""

import pytest
import threading
import time
import requests
from unittest.mock import patch, MagicMock
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from tests.test_mocks import MockGeminiClient
from core.gemini_client import initialize_gemini_client


@pytest.fixture(scope="session")
def mock_gemini_client():
    """Create a mock Gemini client for testing"""
    return MockGeminiClient()


@pytest.fixture(scope="session")
def app_with_mocks(mock_gemini_client):
    """Create Flask app with mocked Gemini client"""
    # Set test environment variables
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['FLASK_DEBUG'] = 'false'
    os.environ['GEMINI_API_KEY'] = 'test_api_key_for_testing'
    
    # Create app
    app = create_app()
    app.config['TESTING'] = True
    
    # Mock the Gemini client
    with patch('core.gemini_client.genai.Client') as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_instance.models = mock_gemini_client
        mock_client_class.return_value = mock_client_instance
        
        # Initialize the mocked client
        initialize_gemini_client()
        
        yield app


@pytest.fixture(scope="session")
def client(app_with_mocks):
    """Create test client"""
    return app_with_mocks.test_client()


@pytest.fixture(scope="session")
def server_url():
    """Get server URL for testing"""
    return "http://127.0.0.1:5001"  # Use different port for testing


@pytest.fixture(scope="session")
def live_server(app_with_mocks, server_url):
    """Start live server for integration testing"""
    # Extract host and port from server_url
    host = "127.0.0.1"
    port = 5001
    
    # Start server in a separate thread
    server_thread = threading.Thread(
        target=lambda: app_with_mocks.run(host=host, port=port, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()
    
    # Wait for server to start
    max_retries = 30
    for _ in range(max_retries):
        try:
            response = requests.get(f"{server_url}/api/health", timeout=1)
            if response.status_code in [200, 503]:  # 503 is also acceptable for health check
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.1)
    else:
        pytest.fail("Server failed to start within timeout")
    
    yield server_url
    
    # Server will be stopped automatically when the process ends


@pytest.fixture
def api_headers():
    """Standard API headers for requests"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture
def sample_requests():
    """Sample request data for testing"""
    from tests.test_mocks import TEST_FIXTURES
    return TEST_FIXTURES


class APITestHelper:
    """Helper class for API testing"""
    
    @staticmethod
    def assert_success_response(response_data):
        """Assert that response is a successful API response"""
        assert "success" in response_data
        assert response_data["success"] is True
        assert "data" in response_data
        assert "timestamp" in response_data
    
    @staticmethod
    def assert_error_response(response_data):
        """Assert that response is an error API response"""
        assert "success" in response_data
        assert response_data["success"] is False
        assert "error" in response_data
        assert "timestamp" in response_data
        assert "code" in response_data["error"]
        assert "message" in response_data["error"]
    
    @staticmethod
    def assert_technique_response(response_data, expected_technique):
        """Assert that response is a valid technique response"""
        APITestHelper.assert_success_response(response_data)
        
        data = response_data["data"]
        assert "technique" in data
        assert data["technique"] == expected_technique
        assert "task" in data
        assert "input" in data
        assert "output" in data
        assert "processing_time" in data
        assert "model" in data
    
    @staticmethod
    def assert_validation_error(response_data):
        """Assert that response is a validation error"""
        APITestHelper.assert_error_response(response_data)
        assert response_data["error"]["code"] == "VALIDATION_ERROR"
        assert "validation_errors" in response_data["error"]["details"]


@pytest.fixture
def api_helper():
    """API test helper fixture"""
    return APITestHelper


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers to tests based on their names
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Mark slow tests
        if any(keyword in item.nodeid for keyword in ["tree_of_thought", "self_consistency"]):
            item.add_marker(pytest.mark.slow)