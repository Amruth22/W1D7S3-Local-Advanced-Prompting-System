"""
Tree-of-Thought (ToT) Prompts
Multiple reasoning path exploration prompts
"""

# Complex Problem Solving ToT Prompt
COMPLEX_PROBLEM_SOLVING = """I need to solve this complex problem by exploring multiple reasoning paths.

Problem: {problem}

Let me explore different approaches:

Approach 1: Direct Analytical Method
- Step 1: Break down the problem into core components
- Step 2: Analyze each component systematically
- Step 3: Synthesize findings into a solution
- Evaluation: Assess effectiveness and feasibility

Approach 2: Creative Innovation Method
- Step 1: Think outside conventional frameworks
- Step 2: Generate unconventional solutions
- Step 3: Adapt creative ideas to practical constraints
- Evaluation: Assess originality and implementability

Approach 3: Systematic Process Method
- Step 1: Follow established methodologies
- Step 2: Apply proven techniques step-by-step
- Step 3: Validate results against best practices
- Evaluation: Assess reliability and completeness

Now let me compare these approaches and select the best path:"""

# Creative Brainstorming ToT Prompt
CREATIVE_BRAINSTORMING = """I need to generate creative solutions by exploring multiple idea paths.

Challenge: {challenge}

Let me explore different creative directions:

Creative Direction 1: Technology-Driven Solutions
- Initial idea: Leverage cutting-edge technology
- Development: Integrate AI, automation, or digital tools
- Potential: High impact through technological innovation

Creative Direction 2: Human-Centered Design
- Initial idea: Focus on user experience and needs
- Development: Design solutions around human behavior
- Potential: High adoption through user-friendly approach

Creative Direction 3: Sustainable Innovation
- Initial idea: Prioritize environmental and social impact
- Development: Create eco-friendly and socially responsible solutions
- Potential: Long-term viability and positive impact

Now let me evaluate and refine the most promising ideas:"""

# Strategic Decision Making ToT Prompt
STRATEGIC_DECISION_MAKING = """I need to make a strategic decision by exploring multiple strategic paths.

Decision: {decision}

Let me explore different strategic options:

Strategy A: Aggressive Growth Approach
- Implementation: Rapid expansion and market capture
- Expected outcomes: High growth, increased market share
- Risks: Resource strain, competitive response
- Success probability: Medium-high with proper execution

Strategy B: Conservative Stability Approach
- Implementation: Steady, measured progress
- Expected outcomes: Sustainable growth, reduced risk
- Risks: Missed opportunities, slower progress
- Success probability: High with consistent execution

Strategy C: Innovation-Focused Approach
- Implementation: Invest heavily in R&D and new solutions
- Expected outcomes: Market differentiation, future positioning
- Risks: Uncertain returns, technology risks
- Success probability: Variable based on innovation success

Now let me compare these strategies and recommend the best approach:"""

# Multi-Perspective Analysis ToT Prompt
MULTI_PERSPECTIVE_ANALYSIS = """I need to analyze this topic from multiple perspectives.

Topic: {topic}

Let me explore different viewpoints:

Perspective 1: Economic Viewpoint
- Key arguments: Focus on financial impact and market dynamics
- Supporting evidence: Economic data, market trends, cost-benefit analysis
- Implications: Financial sustainability and economic growth

Perspective 2: Social Impact Viewpoint
- Key arguments: Consider effects on communities and individuals
- Supporting evidence: Social research, demographic data, case studies
- Implications: Social equity and community well-being

Perspective 3: Technical/Scientific Viewpoint
- Key arguments: Examine technical feasibility and scientific validity
- Supporting evidence: Research studies, technical specifications, expert analysis
- Implications: Technical viability and scientific accuracy

Now let me synthesize these perspectives and identify common ground:"""

# Solution Optimization ToT Prompt
SOLUTION_OPTIMIZATION = """I need to optimize this solution by exploring multiple improvement paths.

Current Solution: {current_solution}

Let me explore different optimization approaches:

Optimization Path 1: Efficiency Enhancement
- Improvements: Streamline processes, reduce waste, automate tasks
- Benefits: Lower costs, faster execution, better resource utilization
- Trade-offs: Initial investment, potential complexity

Optimization Path 2: Quality Improvement
- Improvements: Enhanced features, better user experience, higher standards
- Benefits: Increased satisfaction, competitive advantage, premium positioning
- Trade-offs: Higher costs, longer development time

Optimization Path 3: Scalability Enhancement
- Improvements: Modular design, flexible architecture, growth capacity
- Benefits: Future-ready, adaptable, sustainable growth
- Trade-offs: Over-engineering risk, complexity increase

Now let me determine the best optimization strategy:"""

# Scenario Planning ToT Prompt
SCENARIO_PLANNING = """I need to plan for different scenarios by exploring multiple future paths.

Situation: {situation}

Let me explore different scenarios:

Scenario 1: Optimistic Future
- Key assumptions: Favorable conditions, positive trends continue
- Likely developments: Growth, success, opportunities expand
- Required responses: Scale up, capitalize on opportunities
- Preparation needed: Resource allocation, capacity building

Scenario 2: Pessimistic Future
- Key assumptions: Challenging conditions, negative trends emerge
- Likely developments: Constraints, setbacks, limited opportunities
- Required responses: Risk mitigation, cost reduction, adaptation
- Preparation needed: Contingency planning, resilience building

Scenario 3: Most Likely Future
- Key assumptions: Mixed conditions, balanced trends
- Likely developments: Moderate progress, some challenges
- Required responses: Balanced approach, flexible strategy
- Preparation needed: Adaptive planning, monitoring systems

Now let me develop a comprehensive plan that addresses all scenarios:"""

# Innovation Development ToT Prompt
INNOVATION_DEVELOPMENT = """I need to develop an innovation by exploring multiple development paths.

Innovation Goal: {goal}

Let me explore different development approaches:

Development Path 1: Incremental Innovation
- Core concept: Build upon existing solutions with improvements
- Technical approach: Enhance current technology and methods
- Market potential: Lower risk, established demand
- Feasibility: High, proven foundation

Development Path 2: Disruptive Innovation
- Core concept: Create entirely new approach or solution
- Technical approach: Novel technology or methodology
- Market potential: High impact, new market creation
- Feasibility: Medium, requires validation

Development Path 3: Hybrid Innovation
- Core concept: Combine existing and new elements strategically
- Technical approach: Integrate proven and experimental components
- Market potential: Balanced risk-reward profile
- Feasibility: Medium-high, leverages strengths

Now let me select and refine the most promising innovation path:"""

# Risk Assessment ToT Prompt
RISK_ASSESSMENT = """I need to assess risks by exploring multiple risk scenarios.

Situation: {situation}

Let me explore different risk paths:

Risk Scenario 1: High-Impact, Low-Probability Risks
- Probability: Low likelihood of occurrence
- Impact: Severe consequences if they occur
- Mitigation strategies: Insurance, contingency planning, monitoring
- Contingency plans: Crisis response, recovery procedures

Risk Scenario 2: Medium-Impact, Medium-Probability Risks
- Probability: Moderate likelihood of occurrence
- Impact: Significant but manageable consequences
- Mitigation strategies: Preventive measures, early warning systems
- Contingency plans: Response protocols, resource allocation

Risk Scenario 3: Low-Impact, High-Probability Risks
- Probability: High likelihood of occurrence
- Impact: Minor but frequent consequences
- Mitigation strategies: Process improvements, training, automation
- Contingency plans: Standard procedures, quick fixes

Now let me develop a comprehensive risk management strategy:"""

# Learning Path Exploration ToT Prompt
LEARNING_PATH_EXPLORATION = """I need to explore different learning paths for this topic.

Learning Goal: {goal}

Let me explore different learning approaches:

Learning Path 1: Structured Academic Approach
- Learning method: Formal courses, textbooks, systematic curriculum
- Resources needed: Educational materials, time commitment, possibly instructor
- Timeline: Extended period with structured milestones
- Expected outcomes: Comprehensive understanding, recognized credentials

Learning Path 2: Practical Hands-On Approach
- Learning method: Projects, experimentation, learning by doing
- Resources needed: Tools, practice environments, real-world applications
- Timeline: Flexible, based on project completion
- Expected outcomes: Practical skills, portfolio development

Learning Path 3: Mentorship and Community Approach
- Learning method: Expert guidance, peer learning, community involvement
- Resources needed: Access to mentors, learning communities, networking
- Timeline: Ongoing, relationship-dependent
- Expected outcomes: Industry insights, professional network, personalized guidance

Now let me design the optimal learning strategy:"""