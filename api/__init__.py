"""
API Package
Contains all Flask API route handlers for different prompting techniques
"""

from .few_shot import few_shot_bp
from .chain_of_thought import chain_of_thought_bp
from .tree_of_thought import tree_of_thought_bp
from .self_consistency import self_consistency_bp
from .meta_prompting import meta_prompting_bp

__all__ = [
    'few_shot_bp',
    'chain_of_thought_bp',
    'tree_of_thought_bp',
    'self_consistency_bp',
    'meta_prompting_bp'
]