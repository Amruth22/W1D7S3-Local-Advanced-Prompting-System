"""
Meta-Prompting Prompts
Self-improving and prompt optimization prompts
"""

# Prompt Optimization Meta-Prompt
PROMPT_OPTIMIZATION = """I need to create an effective prompt for the following task: {task}

Current prompt: "{current_prompt}"

Please analyze this prompt and suggest improvements to make it more effective. Consider:
1. Clarity and specificity of instructions
2. Context and background information needed
3. Examples that would help
4. Output format requirements
5. Potential edge cases or ambiguities

Provide an improved version of the prompt that would generate better results."""

# Task Analysis Meta-Prompt
TASK_ANALYSIS = """I need to understand this task better to create an effective prompt for it.

Task: {task}

Please analyze this task and tell me:
1. What are the key requirements?
2. What information does the AI need to complete this task well?
3. What are potential challenges or ambiguities?
4. What examples would be most helpful?
5. What output format would be most useful?

Based on this analysis, suggest the best prompting approach."""

# Prompt Generation Meta-Prompt
PROMPT_GENERATION = """I need to create a prompt for this specific task: {task}

Requirements:
- Target audience: {audience}
- Desired output: {output_type}
- Context: {context}

Please create an effective prompt that:
1. Clearly explains the task
2. Provides necessary context
3. Includes helpful examples if needed
4. Specifies the desired output format
5. Anticipates potential issues

Generate the optimal prompt for this task."""

# Prompt Evaluation Meta-Prompt
PROMPT_EVALUATION = """Please evaluate this prompt for effectiveness:

Task: {task}
Prompt: "{prompt}"

Evaluate the prompt on:
1. Clarity (1-10): How clear are the instructions?
2. Completeness (1-10): Does it include all necessary information?
3. Specificity (1-10): How specific and unambiguous is it?
4. Examples (1-10): Are examples helpful and sufficient?
5. Output format (1-10): Is the desired output clearly specified?

Provide scores and specific suggestions for improvement."""

# Chain Prompting Meta-Prompt
CHAIN_PROMPTING = """I need to break down this complex task into a series of simpler prompts.

Complex task: {task}

Please create a chain of prompts that:
1. Breaks the task into logical steps
2. Each step builds on the previous one
3. Each prompt is clear and focused
4. The sequence leads to the final goal

Provide the sequence of prompts with explanations of how they connect."""

# Conditional Prompting Meta-Prompt
CONDITIONAL_PROMPTING = """I need to create a prompt that adapts based on different conditions.

Base task: {task}
Conditions that might vary: {conditions}

Please create a conditional prompt structure that:
1. Identifies key variables that affect the approach
2. Provides different instructions based on these variables
3. Maintains consistency across all conditions
4. Handles edge cases appropriately

Create the adaptive prompt framework."""

# Prompt Debugging Meta-Prompt
PROMPT_DEBUGGING = """This prompt is not working as expected:

Task: {task}
Current prompt: "{prompt}"
Problem: {problem}
Expected output: {expected}
Actual output: {actual}

Please debug this prompt by:
1. Identifying what's causing the issue
2. Explaining why the current prompt fails
3. Suggesting specific fixes
4. Providing a corrected version

Help me fix this prompt to get the desired results."""

# Style Adaptation Meta-Prompt
STYLE_ADAPTATION = """I need to adapt this prompt for a different style or audience.

Original prompt: "{original_prompt}"
Original style/audience: {original_style}
Target style/audience: {target_style}

Please adapt the prompt by:
1. Adjusting the tone and language
2. Modifying examples to fit the new context
3. Changing the level of detail as appropriate
4. Maintaining the core functionality

Provide the adapted prompt for the new style/audience."""

# Prompt Combination Meta-Prompt
PROMPT_COMBINATION = """I need to combine these different prompting techniques into one effective prompt.

Techniques to combine: {techniques}
Target task: {task}
Specific requirements: {requirements}

Please create a unified prompt that:
1. Incorporates the best aspects of each technique
2. Maintains clarity and focus
3. Avoids redundancy or confusion
4. Maximizes effectiveness for the task

Provide the combined prompt with explanations of how each technique contributes."""

# Prompt Personalization Meta-Prompt
PROMPT_PERSONALIZATION = """I need to personalize this prompt for specific user characteristics.

Base prompt: "{base_prompt}"
User characteristics: {user_characteristics}
Personalization goals: {goals}

Please create a personalized version that:
1. Adapts to the user's knowledge level
2. Uses relevant examples and context
3. Matches the user's communication style
4. Addresses their specific needs

Provide the personalized prompt with explanations of the adaptations made."""

# Prompt Testing Meta-Prompt
PROMPT_TESTING = """I need to create test cases for this prompt to ensure it works well.

Prompt to test: "{prompt}"
Task: {task}

Please create a comprehensive test suite that includes:
1. Typical use cases with expected outputs
2. Edge cases and boundary conditions
3. Potential failure scenarios
4. Variations in input format or style
5. Success criteria for each test case

Provide the test cases with expected results and evaluation criteria."""

# Prompt Iteration Meta-Prompt
PROMPT_ITERATION = """I need to iteratively improve this prompt based on results.

Current prompt: "{current_prompt}"
Task: {task}
Previous results: {results}
Issues identified: {issues}

Please suggest the next iteration that:
1. Addresses the identified issues
2. Builds on what worked well
3. Incorporates lessons learned
4. Moves closer to the ideal prompt

Provide the improved prompt with explanations of the changes made."""

# Domain-Specific Prompt Meta-Prompt
DOMAIN_SPECIFIC_PROMPT = """I need to create a domain-specific prompt for this specialized field.

Domain: {domain}
Task: {task}
Domain expertise required: {expertise_level}

Please create a prompt that:
1. Uses appropriate domain terminology
2. Incorporates domain-specific knowledge
3. Addresses field-specific challenges
4. Meets professional standards for the domain

Provide the domain-specific prompt with explanations of domain considerations."""