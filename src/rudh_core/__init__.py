# src\rudh_core\__init__.py
"""
Rudh AI Companion - Core Module
Main brain and intelligence engine for Rudh
"""

__version__ = "0.1.0"
__author__ = "Sankar Narayanan"
__description__ = "Advanced AI Companion with Emotional Intelligence"

# Main exports
from .core import RudhCore

# Optional imports - only import if modules exist
try:
    from .emotional_intelligence import EmotionalIntelligence
    EMOTIONAL_INTELLIGENCE_AVAILABLE = True
except ImportError:
    EMOTIONAL_INTELLIGENCE_AVAILABLE = False

try:
    from .financial_advisor import FinancialAdvisor
    FINANCIAL_ADVISOR_AVAILABLE = True
except ImportError:
    FINANCIAL_ADVISOR_AVAILABLE = False

# Core exports
__all__ = [
    "RudhCore",
    "EMOTIONAL_INTELLIGENCE_AVAILABLE", 
    "FINANCIAL_ADVISOR_AVAILABLE"
]
