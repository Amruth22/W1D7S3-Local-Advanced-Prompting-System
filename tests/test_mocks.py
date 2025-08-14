"""
Mock Responses for Flask API Testing
Pre-recorded API responses for fast testing without actual API calls
"""

import json
from typing import Dict, Any, List
from unittest.mock import MagicMock
import numpy as np


class MockGeminiResponses:
    """Pre-recorded Gemini API responses for testing"""
    
    # Mock responses for different techniques
    SENTIMENT_RESPONSES = {
        "This smartphone is absolutely amazing! Best purchase ever!": "positive",
        "This product is terrible and doesn't work at all.": "negative", 
        "The weather is okay today. Nothing special.": "neutral",
        "I love this new coffee shop!": "positive",
        "This API is fantastic!": "positive"
    }
    
    MATH_RESPONSES = {
        "If a pizza costs $12 and is cut into 8 slices, how much does each slice cost?": 
        "To find the cost per slice, I need to divide the total cost by the number of slices.\n\nStep 1: Identify the given information\n- Total cost of pizza: $12\n- Number of slices: 8\n\nStep 2: Calculate cost per slice\nCost per slice = Total cost ÷ Number of slices\nCost per slice = $12 ÷ 8 = $1.50\n\nTherefore, each slice costs $1.50.",
        
        "What is 2 + 2?": 
        "Let me solve this step by step.\n\nStep 1: Identify the operation\nWe need to add 2 + 2\n\nStep 2: Perform the addition\n2 + 2 = 4\n\nTherefore, 2 + 2 = 4.",
        
        "A car travels 60 mph for 2.5 hours. How far does it travel?":
        "Let me solve this step by step.\n\nStep 1: Identify the given information\n- Speed: 60 mph\n- Time: 2.5 hours\n\nStep 2: Use the distance formula\nDistance = Speed × Time\nDistance = 60 mph × 2.5 hours = 150 miles\n\nTherefore, the car travels 150 miles."
    }
    
    LOGIC_RESPONSES = {
        "All birds can fly. Penguins are birds. Can penguins fly? Explain the logical issue.":
        "Let me analyze this logical problem step by step.\n\nStep 1: Identify the statements\n- Statement 1: All birds can fly\n- Statement 2: Penguins are birds\n- Statement 3: Penguins cannot fly (implied contradiction)\n\nStep 2: Identify the logical issue\nThis is a classic example of a false premise leading to a logical contradiction.\n\nStep 3: Explain the problem\nThe issue is with the first statement: 'All birds can fly.' This is factually incorrect. While many birds can fly, not all birds have this ability.\n\nConclusion: The reasoning contains a false universal statement. Penguins are indeed birds, but they are flightless birds."
    }
    
    NER_RESPONSES = {
        "Apple Inc. was founded by Steve Jobs in California.":
        "ORGANIZATION: Apple Inc. | PERSON: Steve Jobs | LOCATION: California",
        
        "Tim Cook is the CEO of Apple Inc. based in Cupertino, California.":
        "PERSON: Tim Cook | ORGANIZATION: Apple Inc. | LOCATION: Cupertino, California"
    }
    
    CLASSIFICATION_RESPONSES = {
        "How do I reset my password?": "technical_support",
        "I want to cancel my subscription.": "billing_inquiry",
        "Your service is excellent!": "feedback_positive"
    }
    
    META_PROMPTING_RESPONSES = {
        "optimize_prompt": """Here's an improved version of the prompt:

**Optimized Prompt:**
"Analyze the sentiment of the following text and classify it as positive, negative, or neutral. Consider the overall tone, emotional indicators, and context.

Text: {text}

Please provide:
1. Classification: [positive/negative/neutral]
2. Confidence level: [high/medium/low]
3. Key indicators: [list the words/phrases that influenced your decision]

Classification:"""
    }
    
    TREE_OF_THOUGHT_RESPONSES = {
        "approach_1": "Direct analytical approach: Break down the problem into core components and analyze each systematically. This involves identifying root causes, evaluating current solutions, and developing targeted interventions.",
        
        "approach_2": "Creative problem-solving approach: Use innovative thinking and unconventional methods. This includes brainstorming alternative solutions, thinking outside traditional frameworks, and exploring novel approaches.",
        
        "approach_3": "Systematic breakdown approach: Divide the complex problem into smaller, manageable sub-problems. Address each component individually and then integrate solutions for a comprehensive approach."
    }
    
    SELF_CONSISTENCY_RESPONSES = {
        "What are the main benefits of renewable energy?": [
            "Renewable energy provides numerous benefits including environmental protection, energy independence, job creation, and long-term cost savings.",
            "The main benefits include reduced carbon emissions, sustainable energy supply, economic growth, and improved public health.",
            "Key benefits are: environmental sustainability, energy security, economic opportunities, and reduced pollution."
        ]
    }


class MockGeminiClient:
    """Mock Gemini client that returns pre-recorded responses"""
    
    def __init__(self):
        self.responses = MockGeminiResponses()
        self.call_count = 0
    
    def generate_content(self, model, contents, config):
        """Mock generate_content method"""
        self.call_count += 1
        
        # Extract text from contents
        text = contents[0].parts[0].text if contents and contents[0].parts else ""
        
        # Return appropriate mock response based on text content
        mock_response = self._get_mock_response(text)
        
        # Create mock response object
        response = MagicMock()
        response.candidates = [MagicMock()]
        response.candidates[0].content = MagicMock()
        response.candidates[0].content.parts = [MagicMock()]
        response.candidates[0].content.parts[0].text = mock_response
        
        return response
    
    def _get_mock_response(self, text: str) -> str:
        """Get appropriate mock response based on input text"""
        text_lower = text.lower()
        
        # Sentiment analysis
        for key, response in self.responses.SENTIMENT_RESPONSES.items():
            if key.lower() in text_lower:
                return response
        
        # Math problems
        for key, response in self.responses.MATH_RESPONSES.items():
            if any(word in text_lower for word in ["pizza", "cost", "slice", "2 + 2", "travels", "mph"]):
                return self.responses.MATH_RESPONSES.get(key, "The answer is 42.")
        
        # Logic problems
        for key, response in self.responses.LOGIC_RESPONSES.items():
            if any(word in text_lower for word in ["birds", "penguins", "fly", "logic"]):
                return self.responses.LOGIC_RESPONSES.get(key, "This requires logical analysis.")
        
        # Named Entity Recognition
        for key, response in self.responses.NER_RESPONSES.items():
            if any(word in text_lower for word in ["apple", "steve jobs", "tim cook"]):
                return self.responses.NER_RESPONSES.get(key, "PERSON: John Doe | ORGANIZATION: Company Inc.")
        
        # Text Classification
        for key, response in self.responses.CLASSIFICATION_RESPONSES.items():
            if any(word in text_lower for word in ["password", "reset", "cancel", "subscription", "excellent"]):
                return self.responses.CLASSIFICATION_RESPONSES.get(key, "general_inquiry")
        
        # Meta-prompting
        if any(word in text_lower for word in ["optimize", "improve", "prompt", "better"]):
            return self.responses.META_PROMPTING_RESPONSES["optimize_prompt"]
        
        # Tree of thought
        if "approach 1" in text_lower:
            return self.responses.TREE_OF_THOUGHT_RESPONSES["approach_1"]
        elif "approach 2" in text_lower:
            return self.responses.TREE_OF_THOUGHT_RESPONSES["approach_2"]
        elif "approach 3" in text_lower:
            return self.responses.TREE_OF_THOUGHT_RESPONSES["approach_3"]
        
        # Self-consistency
        for key, responses in self.responses.SELF_CONSISTENCY_RESPONSES.items():
            if any(word in text_lower for word in key.lower().split()):
                return responses[0]  # Return first response
        
        # Default response
        return "This is a mock response for testing purposes."


# Test data fixtures
TEST_FIXTURES = {
    "few_shot_requests": {
        "sentiment": {"text": "This smartphone is absolutely amazing! Best purchase ever!"},
        "math": {"problem": "If a pizza costs $12 and is cut into 8 slices, how much does each slice cost?"},
        "ner": {"text": "Apple Inc. was founded by Steve Jobs in California."},
        "classification": {"text": "How do I reset my password?"}
    },
    
    "chain_of_thought_requests": {
        "math": {"problem": "A car travels 60 mph for 2.5 hours. How far does it travel?"},
        "logic": {"problem": "All birds can fly. Penguins are birds. Can penguins fly? Explain the logical issue."},
        "analysis": {"problem": "What are the potential impacts of artificial intelligence on employment?"}
    },
    
    "tree_of_thought_requests": {
        "explore": {"problem": "How can we reduce plastic waste in our city?", "max_approaches": 3}
    },
    
    "self_consistency_requests": {
        "validate": {"question": "What are the main benefits of renewable energy?", "num_samples": 3}
    },
    
    "meta_prompting_requests": {
        "optimize": {
            "task": "Classify customer feedback",
            "current_prompt": "Is this feedback positive or negative: {text}"
        },
        "analyze": {"task": "Create a comprehensive marketing strategy"}
    }
}


def get_expected_response(request_data: Dict[str, Any], technique: str, task: str) -> str:
    """Get expected response for a given request and technique"""
    responses = MockGeminiResponses()
    
    if technique == "few_shot":
        if task == "sentiment":
            return responses.SENTIMENT_RESPONSES.get(request_data.get("text", ""), "positive")
        elif task == "math":
            return responses.MATH_RESPONSES.get(request_data.get("problem", ""), "The answer is 42.")
        elif task == "ner":
            return responses.NER_RESPONSES.get(request_data.get("text", ""), "PERSON: John Doe")
        elif task == "classification":
            return responses.CLASSIFICATION_RESPONSES.get(request_data.get("text", ""), "general_inquiry")
    
    elif technique == "chain_of_thought":
        if task == "math":
            return responses.MATH_RESPONSES.get(request_data.get("problem", ""), "Step-by-step solution")
        elif task == "logic":
            return responses.LOGIC_RESPONSES.get(request_data.get("problem", ""), "Logical analysis")
    
    elif technique == "meta_prompting":
        if task == "optimize":
            return responses.META_PROMPTING_RESPONSES["optimize_prompt"]
    
    return "Mock response"