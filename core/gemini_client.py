"""
Gemini Client for Flask API
Handles all interactions with Google's Gemini API
"""

import os
import asyncio
import signal
import platform
import threading
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google's Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key (if None, uses environment variable)
            model: Model name to use (if None, uses environment variable)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file or pass it as a parameter.")
        
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = genai.Client(api_key=self.api_key)
        
        # Default configuration
        self.default_temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
        self.default_thinking_budget = int(os.getenv("DEFAULT_THINKING_BUDGET", "5000"))
        
        logger.info(f"Gemini client initialized with model: {self.model}")
    
    def _with_timeout(self, func, timeout_seconds=20):
        """Execute function with timeout (cross-platform)"""
        result = [None]
        exception = [None]
        
        def target():
            try:
                result[0] = func()
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout_seconds)
        
        if thread.is_alive():
            logger.error(f"API call timed out after {timeout_seconds} seconds")
            raise Exception(f"Request timed out after {timeout_seconds} seconds. Please try a simpler query or check your API connection.")
        
        if exception[0]:
            raise exception[0]
        
        return result[0]
    
    def generate_response(
        self, 
        prompt: str, 
        temperature: Optional[float] = None,
        thinking_budget: Optional[int] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a single response from Gemini
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            thinking_budget: Thinking budget for reasoning
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ]
            
            config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_budget=thinking_budget or self.default_thinking_budget
                ),
                temperature=temperature or self.default_temperature
            )
            
            if max_tokens:
                config.max_output_tokens = max_tokens
            
            logger.debug(f"Generating response for prompt: {prompt[:100]}...")
            
            def _make_api_call():
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
                return response.candidates[0].content.parts[0].text
            
            # Use timeout wrapper for API call
            result = self._with_timeout(_make_api_call, timeout_seconds=20)
            logger.debug(f"Generated response: {result[:100]}...")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                raise Exception("Rate limit exceeded. Please wait before making another request.")
            else:
                raise Exception(f"Failed to generate response: {str(e)}")
    
    async def generate_multiple_responses(
        self, 
        prompt: str, 
        num_responses: int = 3,
        temperature: Optional[float] = None,
        thinking_budget: Optional[int] = None
    ) -> List[str]:
        """
        Generate multiple responses asynchronously
        
        Args:
            prompt: Input prompt
            num_responses: Number of responses to generate
            temperature: Sampling temperature
            thinking_budget: Thinking budget for reasoning
            
        Returns:
            List of generated responses
        """
        try:
            logger.debug(f"Generating {num_responses} responses for prompt: {prompt[:100]}...")
            
            tasks = []
            for _ in range(num_responses):
                task = asyncio.create_task(
                    self._async_generate(prompt, temperature, thinking_budget)
                )
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            
            logger.debug(f"Generated {len(responses)} responses successfully")
            return responses
            
        except Exception as e:
            logger.error(f"Error generating multiple responses: {str(e)}")
            raise Exception(f"Failed to generate multiple responses: {str(e)}")
    
    async def _async_generate(
        self, 
        prompt: str, 
        temperature: Optional[float],
        thinking_budget: Optional[int]
    ) -> str:
        """Async wrapper for generate_response"""
        return self.generate_response(prompt, temperature, thinking_budget)
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to Gemini API
        
        Returns:
            Dictionary with connection test results
        """
        try:
            logger.info("Testing Gemini API connection...")
            
            test_response = self.generate_response(
                "Respond with exactly: 'Connection test successful'",
                temperature=0.0,
                thinking_budget=0
            )
            
            success = "successful" in test_response.lower()
            
            result = {
                "gemini_api": success,
                "model": self.model,
                "response": test_response,
                "message": "Connection successful" if success else "Connection failed"
            }
            
            logger.info(f"Connection test result: {result['message']}")
            return result
            
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return {
                "gemini_api": False,
                "model": self.model,
                "error": str(e),
                "message": "Connection failed"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model,
            "default_temperature": self.default_temperature,
            "default_thinking_budget": self.default_thinking_budget,
            "api_key_configured": bool(self.api_key)
        }
    
    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Validate a prompt before sending to API
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            Dictionary with validation results
        """
        issues = []
        
        if not prompt or not prompt.strip():
            issues.append("Prompt is empty")
        
        if len(prompt) > 30000:  # Approximate token limit
            issues.append("Prompt may be too long")
        
        if len(prompt) < 5:
            issues.append("Prompt may be too short")
        
        # Check for potential issues
        if "{" in prompt and "}" not in prompt:
            issues.append("Unmatched curly braces in prompt")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "length": len(prompt),
            "estimated_tokens": len(prompt) // 4  # Rough estimation
        }
    
    def format_prompt_with_context(
        self, 
        template: str, 
        context: Dict[str, Any]
    ) -> str:
        """
        Format a prompt template with context variables
        
        Args:
            template: Prompt template with placeholders
            context: Dictionary of context variables
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.format(**context)
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise ValueError(f"Missing required context variable: {missing_key}")
        except Exception as e:
            raise ValueError(f"Error formatting prompt: {str(e)}")


# Singleton instance for the Flask app
_gemini_client_instance = None

def get_gemini_client() -> GeminiClient:
    """
    Get singleton instance of GeminiClient
    
    Returns:
        GeminiClient instance
    """
    global _gemini_client_instance
    
    if _gemini_client_instance is None:
        _gemini_client_instance = GeminiClient()
    
    return _gemini_client_instance


def initialize_gemini_client(api_key: Optional[str] = None, model: Optional[str] = None) -> GeminiClient:
    """
    Initialize the global Gemini client instance
    
    Args:
        api_key: Gemini API key
        model: Model name
        
    Returns:
        Initialized GeminiClient instance
    """
    global _gemini_client_instance
    _gemini_client_instance = GeminiClient(api_key, model)
    return _gemini_client_instance