"""
Chain-of-Thought (CoT) Prompts
Step-by-step reasoning prompts for complex problem solving
"""

# Mathematical Problem Solving CoT Prompt
MATH_PROBLEM_SOLVING = """Let's solve this step by step.

Problem: {problem}

Step-by-step solution:
1. First, let me understand what we know and what we need to find
2. I'll identify the appropriate method or formula to use
3. Then I'll work through the calculations step by step
4. Finally, I'll check if the answer makes sense

Let me work through this:"""

# Logical Reasoning CoT Prompt
LOGICAL_REASONING = """Let's approach this logical problem step by step.

Problem: {problem}

Step-by-step logical reasoning:
1. First, I'll identify all the given information and constraints
2. Then I'll analyze the relationships between different elements
3. I'll apply logical rules and deduction step by step
4. Finally, I'll verify that my conclusion follows logically

Let me reason through this:"""

# Complex Analysis CoT Prompt
COMPLEX_ANALYSIS = """Let's analyze this complex problem systematically.

Problem: {problem}

Step-by-step analysis:
1. First, I'll break down the problem into smaller components
2. I'll examine each component and its relationships
3. I'll consider different perspectives and approaches
4. I'll synthesize the information to reach a conclusion
5. Finally, I'll evaluate the strength of my analysis

Let me work through this analysis:"""

# Decision Making CoT Prompt
DECISION_MAKING = """Let's approach this decision systematically.

Decision: {decision}

Step-by-step decision process:
1. First, I'll clearly define the decision that needs to be made
2. I'll identify all available options
3. I'll list the relevant criteria for evaluation
4. I'll analyze each option against these criteria
5. I'll weigh the pros and cons
6. Finally, I'll make a reasoned recommendation

Let me work through this decision:"""

# Problem Solving CoT Prompt
PROBLEM_SOLVING = """Let's solve this problem step by step.

Problem: {problem}

Step-by-step problem solving:
1. First, I'll clearly understand and define the problem
2. I'll gather and organize all relevant information
3. I'll brainstorm possible solutions or approaches
4. I'll evaluate each approach for feasibility and effectiveness
5. I'll select the best approach and implement it
6. Finally, I'll verify that the solution addresses the original problem

Let me work through this:"""

# Reading Comprehension CoT Prompt
READING_COMPREHENSION = """Let's analyze this text step by step to answer the question.

Text: {text}

Question: {question}

Step-by-step analysis:
1. First, I'll read and understand the main ideas in the text
2. I'll identify key details and information relevant to the question
3. I'll analyze how these details relate to what's being asked
4. I'll formulate a complete answer based on the evidence
5. Finally, I'll check that my answer directly addresses the question

Let me work through this:"""

# Scientific Reasoning CoT Prompt
SCIENTIFIC_REASONING = """Let's apply scientific reasoning to this problem step by step.

Problem: {problem}

Step-by-step scientific reasoning:
1. First, I'll state the hypothesis or question clearly
2. I'll examine the available evidence and data
3. I'll consider what we know from scientific principles
4. I'll analyze cause-and-effect relationships
5. I'll draw conclusions based on the evidence
6. Finally, I'll consider the limitations and confidence level of my conclusion

Let me work through this scientifically:"""

# Creative Problem Solving CoT Prompt
CREATIVE_PROBLEM_SOLVING = """Let's approach this creative challenge step by step.

Challenge: {challenge}

Step-by-step creative process:
1. First, I'll fully understand the challenge and any constraints
2. I'll brainstorm multiple creative approaches without judgment
3. I'll explore unconventional and innovative solutions
4. I'll evaluate each idea for originality and feasibility
5. I'll refine and develop the most promising concepts
6. Finally, I'll present creative solutions with clear reasoning

Let me work through this creatively:"""

# Ethical Reasoning CoT Prompt
ETHICAL_REASONING = """Let's examine this ethical dilemma step by step.

Dilemma: {dilemma}

Step-by-step ethical analysis:
1. First, I'll identify the key ethical issues and stakeholders involved
2. I'll consider different ethical frameworks and principles
3. I'll analyze the potential consequences of different actions
4. I'll examine the rights, duties, and responsibilities involved
5. I'll weigh competing values and interests
6. Finally, I'll provide a reasoned ethical judgment

Let me work through this ethical analysis:"""

# Strategic Planning CoT Prompt
STRATEGIC_PLANNING = """Let's develop a strategic plan step by step.

Goal: {goal}

Step-by-step strategic planning:
1. First, I'll clearly define the strategic goal and success criteria
2. I'll analyze the current situation and available resources
3. I'll identify opportunities, challenges, and constraints
4. I'll develop multiple strategic options
5. I'll evaluate each option for feasibility and impact
6. I'll create an implementation plan with specific steps
7. Finally, I'll consider how to monitor progress and adapt

Let me work through this strategic planning:"""

# Troubleshooting CoT Prompt
TROUBLESHOOTING = """Let's troubleshoot this problem step by step.

Problem: {problem}

Step-by-step troubleshooting:
1. First, I'll clearly identify and describe the problem symptoms
2. I'll gather relevant information about when and how it occurs
3. I'll brainstorm possible causes based on the symptoms
4. I'll systematically test each potential cause
5. I'll identify the root cause of the problem
6. I'll develop and implement a solution
7. Finally, I'll verify that the solution resolves the problem

Let me work through this troubleshooting:"""

# Research Analysis CoT Prompt
RESEARCH_ANALYSIS = """Let's analyze this research question step by step.

Research Question: {question}

Step-by-step research analysis:
1. First, I'll break down the research question into key components
2. I'll identify what information and evidence is needed
3. I'll examine available sources and data systematically
4. I'll analyze patterns, trends, and relationships in the information
5. I'll consider alternative interpretations and limitations
6. I'll synthesize findings into clear conclusions
7. Finally, I'll assess the strength of evidence and confidence level

Let me work through this research analysis:"""