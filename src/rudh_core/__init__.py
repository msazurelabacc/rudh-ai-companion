"""
Rudh - The Eternal AI Companion
Core module initialization

Version: 0.1.0
Author: Sankar Narayanan
Description: Advanced AI Companion with Emotional Intelligence
"""

__version__ = "0.1.0"
__author__ = "Sankar Narayanan"
__description__ = "Advanced AI Companion with Emotional Intelligence"

from .core import RudhCore
from .personality import RudhPersonality

__all__ = ["RudhCore", "RudhPersonality"]
