"""
Few-shot Learning Prompts
Simple prompt templates for few-shot learning with examples
"""

# Sentiment Classification Few-shot Prompt
SENTIMENT_CLASSIFICATION = """Here are some examples of sentiment classification:

Example 1:
Input: "I love this product! It's amazing and works perfectly."
Output: positive
Explanation: The text contains positive words like 'love', 'amazing', and 'perfectly'.

Example 2:
Input: "This is terrible. I hate it and want my money back."
Output: negative
Explanation: The text contains negative words like 'terrible', 'hate', and expresses dissatisfaction.

Example 3:
Input: "The weather is okay today. Nothing special."
Output: neutral
Explanation: The text is neither particularly positive nor negative, using neutral language.

Now, please classify the sentiment of this text: "{text}"
Output:"""

# Named Entity Recognition Few-shot Prompt
NAMED_ENTITY_RECOGNITION = """Here are some examples of named entity recognition:

Example 1:
Input: "John Smith works at Google in Mountain View, California."
Output: PERSON: John Smith | ORGANIZATION: Google | LOCATION: Mountain View, California

Example 2:
Input: "Apple Inc. was founded by Steve Jobs on April 1, 1976."
Output: ORGANIZATION: Apple Inc. | PERSON: Steve Jobs | DATE: April 1, 1976

Example 3:
Input: "The meeting is scheduled for tomorrow at 3 PM in New York."
Output: TIME: tomorrow at 3 PM | LOCATION: New York

Now, please extract entities from this text: "{text}"
Output:"""

# Text Classification Few-shot Prompt
TEXT_CLASSIFICATION = """Here are some examples of text classification:

Example 1:
Input: "How do I reset my password?"
Output: technical_support
Explanation: User is asking for help with a technical issue.

Example 2:
Input: "I want to cancel my subscription and get a refund."
Output: billing_inquiry
Explanation: User is asking about billing and subscription matters.

Example 3:
Input: "Your service is excellent! Keep up the good work."
Output: feedback_positive
Explanation: User is providing positive feedback about the service.

Now, please classify this text: "{text}"
Output:"""

# Math Word Problems Few-shot Prompt
MATH_WORD_PROBLEMS = """Here are some examples of solving math word problems:

Example 1:
Input: "Sarah has 15 apples. She gives 7 to her friend. How many apples does she have left?"
Output: 8 apples
Explanation: Sarah starts with 15 apples. She gives away 7 apples. 15 - 7 = 8 apples remaining.

Example 2:
Input: "A rectangle has a length of 8 meters and width of 5 meters. What is its area?"
Output: 40 square meters
Explanation: Area of rectangle = length × width. Area = 8 × 5 = 40 square meters.

Example 3:
Input: "If a car travels 60 miles per hour for 3 hours, how far does it travel?"
Output: 180 miles
Explanation: Distance = speed × time. Distance = 60 mph × 3 hours = 180 miles.

Now, please solve this math problem: "{problem}"
Output:"""

# Language Translation Few-shot Prompt
LANGUAGE_TRANSLATION = """Here are some examples of language translation:

Example 1:
Input: "Hello, how are you?" (English to Spanish)
Output: "Hola, ¿cómo estás?"

Example 2:
Input: "Thank you very much" (English to French)
Output: "Merci beaucoup"

Example 3:
Input: "Good morning" (English to German)
Output: "Guten Morgen"

Now, please translate this text: "{text}" (English to {target_language})
Output:"""

# Code Generation Few-shot Prompt
CODE_GENERATION = """Here are some examples of code generation:

Example 1:
Input: "Create a function to calculate the factorial of a number"
Output: 
```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

Example 2:
Input: "Write a function to check if a string is a palindrome"
Output:
```python
def is_palindrome(s):
    s = s.lower().replace(' ', '')
    return s == s[::-1]
```

Example 3:
Input: "Create a function to find the maximum number in a list"
Output:
```python
def find_max(numbers):
    if not numbers:
        return None
    return max(numbers)
```

Now, please generate code for: "{task}"
Output:"""

# Question Answering Few-shot Prompt
QUESTION_ANSWERING = """Here are some examples of question answering:

Example 1:
Context: "The Eiffel Tower is located in Paris, France. It was built in 1889 and stands 324 meters tall."
Question: "How tall is the Eiffel Tower?"
Answer: The Eiffel Tower is 324 meters tall.

Example 2:
Context: "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991."
Question: "Who created Python?"
Answer: Python was created by Guido van Rossum.

Example 3:
Context: "The human heart has four chambers: two atria and two ventricles. It pumps blood throughout the body."
Question: "How many chambers does the human heart have?"
Answer: The human heart has four chambers.

Context: "{context}"
Question: "{question}"
Answer:"""