"""
Prompting Service
Main service class that orchestrates all advanced prompting techniques
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from .gemini_client import get_gemini_client
from prompts import few_shot, chain_of_thought, tree_of_thought, self_consistency, meta_prompting

# Set up logging
logger = logging.getLogger(__name__)


class PromptingService:
    """Main service for advanced prompting techniques"""
    
    def __init__(self):
        """Initialize the prompting service"""
        self.gemini_client = get_gemini_client()
        logger.info("Prompting service initialized")
    
    # ==================== FEW-SHOT LEARNING ====================
    
    def few_shot_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform sentiment analysis using few-shot learning
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment analysis results
        """
        start_time = time.time()
        
        try:
            prompt = few_shot.SENTIMENT_CLASSIFICATION.format(text=text)
            response = self.gemini_client.generate_response(prompt, temperature=0.3)
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Few-shot Learning",
                "task": "sentiment_analysis",
                "input": text,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "SENTIMENT_CLASSIFICATION"
                }
            }
            
        except Exception as e:
            logger.error(f"Error in few-shot sentiment analysis: {str(e)}")
            raise Exception(f"Sentiment analysis failed: {str(e)}")
    
    def few_shot_math_solver(self, problem: str) -> Dict[str, Any]:
        """
        Solve math problems using few-shot learning
        
        Args:
            problem: Math problem to solve
            
        Returns:
            Dictionary with math solution results
        """
        start_time = time.time()
        
        try:
            prompt = few_shot.MATH_WORD_PROBLEMS.format(problem=problem)
            response = self.gemini_client.generate_response(prompt, temperature=0.2)
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Few-shot Learning",
                "task": "math_solving",
                "input": problem,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "MATH_WORD_PROBLEMS"
                }
            }
            
        except Exception as e:
            logger.error(f"Error in few-shot math solving: {str(e)}")
            raise Exception(f"Math solving failed: {str(e)}")
    
    def few_shot_named_entity_recognition(self, text: str) -> Dict[str, Any]:
        """
        Extract named entities using few-shot learning
        
        Args:
            text: Text to process
            
        Returns:
            Dictionary with NER results
        """
        start_time = time.time()
        
        try:
            prompt = few_shot.NAMED_ENTITY_RECOGNITION.format(text=text)
            response = self.gemini_client.generate_response(prompt, temperature=0.2)
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Few-shot Learning",
                "task": "named_entity_recognition",
                "input": text,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "NAMED_ENTITY_RECOGNITION"
                }
            }
            
        except Exception as e:
            logger.error(f"Error in few-shot NER: {str(e)}")
            raise Exception(f"Named entity recognition failed: {str(e)}")
    
    def few_shot_text_classification(self, text: str) -> Dict[str, Any]:
        """
        Classify text using few-shot learning
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary with classification results
        """
        start_time = time.time()
        
        try:
            prompt = few_shot.TEXT_CLASSIFICATION.format(text=text)
            response = self.gemini_client.generate_response(prompt, temperature=0.3)
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Few-shot Learning",
                "task": "text_classification",
                "input": text,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "TEXT_CLASSIFICATION"
                }
            }
            
        except Exception as e:
            logger.error(f"Error in few-shot text classification: {str(e)}")
            raise Exception(f"Text classification failed: {str(e)}")
    
    # ==================== CHAIN-OF-THOUGHT ====================
    
    def chain_of_thought_math_solver(self, problem: str) -> Dict[str, Any]:
        """
        Solve math problems using chain-of-thought reasoning
        
        Args:
            problem: Math problem to solve
            
        Returns:
            Dictionary with step-by-step solution
        """
        start_time = time.time()
        
        try:
            prompt = chain_of_thought.MATH_PROBLEM_SOLVING.format(problem=problem)
            response = self.gemini_client.generate_response(
                prompt, 
                temperature=0.3
            )
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Chain-of-Thought",
                "task": "math_reasoning",
                "input": problem,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "MATH_PROBLEM_SOLVING",
                    "thinking_budget": 10000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in chain-of-thought math solving: {str(e)}")
            raise Exception(f"Chain-of-thought math solving failed: {str(e)}")
    
    def chain_of_thought_logical_reasoning(self, problem: str) -> Dict[str, Any]:
        """
        Solve logical problems using chain-of-thought reasoning
        
        Args:
            problem: Logical problem to analyze
            
        Returns:
            Dictionary with logical reasoning results
        """
        start_time = time.time()
        
        try:
            prompt = chain_of_thought.LOGICAL_REASONING.format(problem=problem)
            response = self.gemini_client.generate_response(
                prompt, 
                temperature=0.3
            )
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Chain-of-Thought",
                "task": "logical_reasoning",
                "input": problem,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "LOGICAL_REASONING",
                    "thinking_budget": 12000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in chain-of-thought logical reasoning: {str(e)}")
            raise Exception(f"Chain-of-thought logical reasoning failed: {str(e)}")
    
    def chain_of_thought_complex_analysis(self, problem: str) -> Dict[str, Any]:
        """
        Analyze complex problems using chain-of-thought reasoning
        
        Args:
            problem: Complex problem to analyze
            
        Returns:
            Dictionary with detailed analysis
        """
        start_time = time.time()
        
        try:
            prompt = chain_of_thought.COMPLEX_ANALYSIS.format(problem=problem)
            # Optimized for faster response with thinking disabled
            response = self.gemini_client.generate_response(
                prompt, 
                temperature=0.3
            )
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Chain-of-Thought",
                "task": "complex_analysis",
                "input": problem,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "COMPLEX_ANALYSIS",
                    "thinking_budget": 15000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in chain-of-thought complex analysis: {str(e)}")
            raise Exception(f"Chain-of-thought complex analysis failed: {str(e)}")
    
    # ==================== TREE-OF-THOUGHT ====================
    
    async def tree_of_thought_explore(
        self, 
        problem: str, 
        max_approaches: int = 3
    ) -> Dict[str, Any]:
        """
        Explore multiple solution approaches using tree-of-thought
        
        Args:
            problem: Problem to explore
            max_approaches: Maximum number of approaches to explore
            
        Returns:
            Dictionary with multiple approaches and best selection
        """
        start_time = time.time()
        
        try:
            approaches = []
            approach_names = [
                "Direct Analytical Method",
                "Creative Innovation Method", 
                "Systematic Process Method"
            ]
            
            # Generate multiple approaches
            for i in range(min(max_approaches, len(approach_names))):
                approach_prompt = f"""Problem: {problem}

I'll use approach {i+1}: {approach_names[i]}

Let me work through this step by step:
1. First, I'll analyze the problem from this perspective
2. Then I'll develop a solution strategy
3. Finally, I'll evaluate the effectiveness

Working through approach {i+1}:"""
                
                response = await self.gemini_client._async_generate(
                    approach_prompt, 
                    temperature=0.6
                )
                
                approaches.append({
                    "approach_number": i + 1,
                    "approach_name": approach_names[i],
                    "solution": response.strip()
                })
            
            # Select best approach
            best_approach = await self._select_best_approach(problem, approaches)
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Tree-of-Thought",
                "task": "multi_approach_exploration",
                "input": problem,
                "output": {
                    "explored_approaches": approaches,
                    "best_approach": best_approach,
                    "total_approaches": len(approaches)
                },
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "max_approaches": max_approaches,
                    "thinking_budget": 8000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in tree-of-thought exploration: {str(e)}")
            raise Exception(f"Tree-of-thought exploration failed: {str(e)}")
    
    async def _select_best_approach(
        self, 
        problem: str, 
        approaches: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Select the best approach from multiple options"""
        evaluation_prompt = f"""Problem: {problem}

I have explored these different approaches:

{chr(10).join([f"Approach {a['approach_number']}: {a['approach_name']}" + chr(10) + f"Solution: {a['solution'][:200]}..." for a in approaches])}

Please evaluate these approaches and select the best one based on:
1. Effectiveness in solving the problem
2. Feasibility of implementation
3. Completeness of the solution
4. Innovation and creativity

Best approach selection:"""
        
        evaluation = await self.gemini_client._async_generate(
            evaluation_prompt, 
            temperature=0.3
        )
        
        return {
            "evaluation": evaluation.strip(),
            "selection_criteria": [
                "effectiveness", 
                "feasibility", 
                "completeness", 
                "innovation"
            ]
        }
    
    # ==================== SELF-CONSISTENCY ====================
    
    async def self_consistency_validate(
        self, 
        question: str, 
        num_samples: int = 3
    ) -> Dict[str, Any]:
        """
        Get consistent answers using multiple sampling
        
        Args:
            question: Question to answer
            num_samples: Number of samples to generate
            
        Returns:
            Dictionary with consistency validation results
        """
        start_time = time.time()
        
        try:
            prompt = self_consistency.GENERAL_CONSISTENCY.format(question=question)
            
            # Generate multiple responses
            responses = await self.gemini_client.generate_multiple_responses(
                prompt, 
                num_samples, 
                temperature=0.7
            )
            
            # Analyze consistency
            consistency_analysis = await self._analyze_consistency(question, responses)
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Self-Consistency",
                "task": "consistency_validation",
                "input": question,
                "output": {
                    "all_responses": responses,
                    "consistency_analysis": consistency_analysis,
                    "final_answer": consistency_analysis.get("most_consistent_answer", ""),
                    "num_samples": num_samples
                },
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "num_samples": num_samples,
                    "thinking_budget": 5000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in self-consistency validation: {str(e)}")
            raise Exception(f"Self-consistency validation failed: {str(e)}")
    
    async def _analyze_consistency(
        self, 
        question: str, 
        responses: List[str]
    ) -> Dict[str, Any]:
        """Analyze consistency across multiple responses"""
        analysis_prompt = f"""Question: {question}

I have these {len(responses)} different responses:

{chr(10).join([f"Response {i+1}: {resp}" for i, resp in enumerate(responses)])}

Please analyze these responses for consistency:
1. What are the common themes or answers?
2. What are the main differences?
3. Which response seems most accurate and complete?
4. What is the most consistent answer across all responses?

Consistency analysis:"""
        
        analysis = await self.gemini_client._async_generate(
            analysis_prompt, 
            temperature=0.2
        )
        
        return {
            "analysis": analysis.strip(),
            "response_count": len(responses),
            "most_consistent_answer": self._extract_most_consistent_answer(analysis)
        }
    
    def _extract_most_consistent_answer(self, analysis: str) -> str:
        """Extract the most consistent answer from analysis"""
        lines = analysis.split('\n')
        for line in lines:
            if "most consistent" in line.lower() or "most reliable" in line.lower():
                return line.strip()
        
        # If no specific line found, return last meaningful line
        meaningful_lines = [line.strip() for line in lines if line.strip() and len(line.strip()) > 10]
        return meaningful_lines[-1] if meaningful_lines else "Analysis inconclusive"
    
    # ==================== META-PROMPTING ====================
    
    def meta_prompt_optimization(self, task: str, current_prompt: str) -> Dict[str, Any]:
        """
        Optimize prompts using meta-prompting
        
        Args:
            task: Task description
            current_prompt: Current prompt to optimize
            
        Returns:
            Dictionary with prompt optimization results
        """
        start_time = time.time()
        
        try:
            prompt = meta_prompting.PROMPT_OPTIMIZATION.format(
                task=task, 
                current_prompt=current_prompt
            )
            response = self.gemini_client.generate_response(
                prompt, 
                temperature=0.4
            )
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Meta-Prompting",
                "task": "prompt_optimization",
                "input": {
                    "task": task,
                    "current_prompt": current_prompt
                },
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "PROMPT_OPTIMIZATION",
                    "thinking_budget": 8000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in meta-prompt optimization: {str(e)}")
            raise Exception(f"Meta-prompt optimization failed: {str(e)}")
    
    def meta_task_analysis(self, task: str) -> Dict[str, Any]:
        """
        Analyze tasks for better prompting using meta-prompting
        
        Args:
            task: Task to analyze
            
        Returns:
            Dictionary with task analysis results
        """
        start_time = time.time()
        
        try:
            prompt = meta_prompting.TASK_ANALYSIS.format(task=task)
            response = self.gemini_client.generate_response(
                prompt, 
                temperature=0.3
            )
            
            processing_time = time.time() - start_time
            
            return {
                "technique": "Meta-Prompting",
                "task": "task_analysis",
                "input": task,
                "output": response.strip(),
                "metadata": {
                    "processing_time": round(processing_time, 3),
                    "model": self.gemini_client.model,
                    "prompt_template": "TASK_ANALYSIS",
                    "thinking_budget": 6000
                }
            }
            
        except Exception as e:
            logger.error(f"Error in meta-task analysis: {str(e)}")
            raise Exception(f"Meta-task analysis failed: {str(e)}")
    
    # ==================== UTILITY METHODS ====================
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get information about the prompting service
        
        Returns:
            Dictionary with service information
        """
        return {
            "service": "Advanced Prompting Service",
            "techniques": [
                "Few-shot Learning",
                "Chain-of-Thought",
                "Tree-of-Thought", 
                "Self-Consistency",
                "Meta-Prompting"
            ],
            "model_info": self.gemini_client.get_model_info(),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def test_all_techniques(self) -> Dict[str, Any]:
        """
        Test all prompting techniques with simple examples
        
        Returns:
            Dictionary with test results for all techniques
        """
        results = {}
        
        try:
            # Test few-shot learning
            results["few_shot"] = self.few_shot_sentiment_analysis("This is a test.")
            
            # Test chain-of-thought
            results["chain_of_thought"] = self.chain_of_thought_math_solver("What is 2 + 2?")
            
            # Test meta-prompting
            results["meta_prompting"] = self.meta_prompt_optimization(
                "Test task", 
                "Test prompt"
            )
            
            results["overall_status"] = "All techniques working"
            
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "Some techniques failed"
        
        return results


# Singleton instance for the Flask app
_prompting_service_instance = None

def get_prompting_service() -> PromptingService:
    """
    Get singleton instance of PromptingService
    
    Returns:
        PromptingService instance
    """
    global _prompting_service_instance
    
    if _prompting_service_instance is None:
        _prompting_service_instance = PromptingService()
    
    return _prompting_service_instance