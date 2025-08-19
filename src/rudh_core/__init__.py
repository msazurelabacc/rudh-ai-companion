"""
Rudh AI Core Package - Phase 2.2
Enhanced emotion detection and context-aware AI companion
"""

__version__ = "2.2.0"
__author__ = "Rudh AI Project"

# Import Phase 2.2 components
try:
    from .emotion_engine import EnhancedEmotionEngine
    from .context_engine import AdvancedContextEngine, ConversationContext, ResponseStrategy
    from .core import EnhancedRudhCore
    
    # Backward compatibility - alias old names to new ones
    RudhCore = EnhancedRudhCore  # For backward compatibility
    
    __all__ = [
        'EnhancedEmotionEngine',
        'AdvancedContextEngine', 
        'ConversationContext',
        'ResponseStrategy',
        'EnhancedRudhCore',
        'RudhCore'  # Backward compatibility
    ]
    
except ImportError as e:
    print(f"Warning: Could not import some Rudh components: {e}")
    __all__ = []

# Package information
def get_version():
    """Get the current version of Rudh AI"""
    return __version__

def get_info():
    """Get package information"""
    return {
        'name': 'Rudh AI Companion',
        'version': __version__,
        'description': 'Advanced emotion detection and context-aware AI companion',
        'phase': '2.2 - Context-Aware Response Generation',
        'features': [
            '16+ emotion types with confidence scoring',
            'Advanced context analysis (7 topic categories)',
            'Intelligent response strategies (5 types)',
            'Multi-turn conversation awareness',
            'User personality learning',
            'Real-time performance analytics'
        ]
    }