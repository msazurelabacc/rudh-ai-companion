# src/rudh_core/emotion_engine.py
"""
Rudh AI Enhanced Emotion Detection Engine - Phase 2.1 FIXED
Advanced emotion recognition with 15+ emotions and optimized confidence scoring
"""

import re
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from datetime import datetime

@dataclass
class EmotionResult:
    """Emotion detection result with confidence and context"""
    primary_emotion: str
    confidence: float
    secondary_emotions: List[Tuple[str, float]]
    emotional_intensity: str  # low, medium, high
    context_keywords: List[str]
    timestamp: datetime

class EnhancedEmotionEngine:
    """
    Advanced emotion detection engine for Rudh AI
    Supports 15+ emotions with contextual understanding
    FIXED VERSION with optimized confidence scoring
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Enhanced emotion patterns with optimized scoring
        self.emotion_patterns = {
            # Core Emotions (High Confidence)
            'joyful': {
                'keywords': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'fantastic', 
                           'great', 'excellent', 'love', 'thrilled', 'delighted', 'cheerful'],
                'patterns': [r'\b(so happy|feeling great|amazing day|love this)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 2.0, 'incredibly': 1.8, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'upset', 'disappointed', 
                           'heartbroken', 'miserable', 'gloomy', 'blue', 'melancholy'],
                'patterns': [r'\b(feeling down|so sad|heart broken|really disappointed)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 2.0, 'deeply': 1.8, 'so': 1.3, 'really': 1.3},
                'base_weight': 1.0
            },
            
            'anxious': {
                'keywords': ['anxious', 'nervous', 'worried', 'stressed', 'tense', 
                           'panicked', 'uneasy', 'concerned', 'troubled', 'restless', 'panic'],
                'patterns': [r'\b(so worried|really stressed|panic|anxiety|nervous about)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 2.0, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'angry': {
                'keywords': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 
                           'frustrated', 'outraged', 'livid', 'enraged', 'pissed'],
                'patterns': [r'\b(so angry|really mad|frustrated with|pissed off)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 2.0, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'fearful': {
                'keywords': ['scared', 'afraid', 'frightened', 'terrified', 'fearful', 
                           'nervous', 'apprehensive', 'worried', 'concerned'],
                'patterns': [r'\b(so scared|really afraid|terrified of|fear that)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 2.0, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            # Advanced Emotions (Medium-High Confidence)
            'grateful': {
                'keywords': ['thank', 'thanks', 'grateful', 'appreciate', 'blessed', 
                           'thankful', 'recognition', 'acknowledgment'],
                'patterns': [r'\b(thank you|so grateful|really appreciate|blessed to)\b'],
                'intensity_modifiers': {'very': 1.4, 'extremely': 1.8, 'really': 1.3, 'so': 1.2},
                'base_weight': 1.2
            },
            
            'confused': {
                'keywords': ['confused', 'puzzled', 'lost', 'unclear', 'bewildered', 
                           'perplexed', 'baffled', 'uncertain', 'unsure', 'understand'],
                'patterns': [r'\b(so confused|really lost|not sure|don\'t understand)\b'],
                'intensity_modifiers': {'very': 1.4, 'really': 1.3, 'completely': 1.6, 'so': 1.2},
                'base_weight': 1.1
            },
            
            'excited': {
                'keywords': ['excited', 'thrilled', 'pumped', 'enthusiastic', 'eager', 
                           'energetic', 'hyped', 'stoked', 'elated'],
                'patterns': [r'\b(so excited|really thrilled|can\'t wait|pumped about)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 2.0, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'disappointed': {
                'keywords': ['disappointed', 'let down', 'failed', 'missed', 'regret', 
                           'unfortunate', 'setback', 'bummer'],
                'patterns': [r'\b(so disappointed|really let down|failed to|missed out)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 1.8, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'hopeful': {
                'keywords': ['hopeful', 'optimistic', 'positive', 'confident', 'expecting', 
                           'looking forward', 'anticipating', 'promising'],
                'patterns': [r'\b(feeling hopeful|optimistic about|looking forward|confident that)\b'],
                'intensity_modifiers': {'very': 1.3, 'really': 1.2, 'quite': 1.1, 'so': 1.2},
                'base_weight': 1.0
            },
            
            'lonely': {
                'keywords': ['lonely', 'alone', 'isolated', 'solitary', 'abandoned', 
                           'disconnected', 'empty', 'missing'],
                'patterns': [r'\b(feel lonely|so alone|isolated from|missing people)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 1.8, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'proud': {
                'keywords': ['proud', 'accomplished', 'achieved', 'successful', 'satisfied', 
                           'fulfilled', 'victorious', 'pleased'],
                'patterns': [r'\b(so proud|really accomplished|achieved my|successful in)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 1.8, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'guilty': {
                'keywords': ['guilty', 'ashamed', 'regret', 'sorry', 'fault', 
                           'blame', 'responsible', 'apologetic'],
                'patterns': [r'\b(feel guilty|so ashamed|my fault|sorry for|regret that)\b'],
                'intensity_modifiers': {'very': 1.5, 'extremely': 1.8, 'really': 1.4, 'so': 1.3},
                'base_weight': 1.0
            },
            
            'surprised': {
                'keywords': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected', 
                           'sudden', 'wow', 'incredible'],
                'patterns': [r'\b(so surprised|really shocked|can\'t believe|unexpected news)\b'],
                'intensity_modifiers': {'very': 1.4, 'extremely': 1.8, 'really': 1.3, 'so': 1.2},
                'base_weight': 1.0
            },
            
            'content': {
                'keywords': ['content', 'satisfied', 'peaceful', 'calm', 'serene', 
                           'comfortable', 'relaxed', 'at ease'],
                'patterns': [r'\b(feeling content|quite satisfied|peaceful moment|calm and)\b'],
                'intensity_modifiers': {'very': 1.3, 'quite': 0.8, 'really': 1.2},
                'base_weight': 0.9
            },
            
            # Neutral emotion
            'neutral': {
                'keywords': ['okay', 'fine', 'normal', 'regular', 'usual', 'average'],
                'patterns': [r'\b(doing okay|feeling fine|nothing special|just normal)\b'],
                'intensity_modifiers': {},
                'base_weight': 0.8
            }
        }
        
        # Adjusted intensity level thresholds for better detection
        self.intensity_thresholds = {
            'low': (0.0, 0.35),
            'medium': (0.35, 0.65),
            'high': (0.65, 1.0)
        }
        
        # Context categories for better understanding
        self.context_categories = {
            'work': ['work', 'job', 'career', 'office', 'boss', 'colleague', 'project', 'meeting'],
            'family': ['family', 'mother', 'father', 'parent', 'child', 'sibling', 'relative'],
            'relationship': ['relationship', 'partner', 'boyfriend', 'girlfriend', 'spouse', 'love'],
            'health': ['health', 'sick', 'doctor', 'medicine', 'hospital', 'pain', 'wellness'],
            'money': ['money', 'financial', 'budget', 'expensive', 'cost', 'income', 'investment'],
            'social': ['friends', 'social', 'party', 'gathering', 'people', 'community'],
            'personal': ['personal', 'self', 'myself', 'individual', 'private', 'own']
        }

    def detect_emotion(self, text: str, context: Optional[Dict] = None) -> EmotionResult:
        """
        Detect emotions in text with enhanced accuracy and confidence scoring
        FIXED VERSION with optimized scoring algorithm
        """
        if not text.strip():
            return self._create_neutral_result()
        
        text_lower = text.lower().strip()
        emotion_scores = {}
        context_keywords = []
        
        # Analyze each emotion pattern with improved scoring
        for emotion, patterns in self.emotion_patterns.items():
            score = self._calculate_emotion_score_fixed(text_lower, patterns)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Detect context categories
        context_keywords = self._detect_context(text_lower)
        
        # If no emotions detected, return neutral
        if not emotion_scores:
            return self._create_neutral_result(context_keywords)
        
        # Sort emotions by score
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        primary_emotion, primary_score = sorted_emotions[0]
        
        # Get secondary emotions (top 3, excluding primary)
        secondary_emotions = [(emotion, score) for emotion, score in sorted_emotions[1:4] if score > 0.2]
        
        # Determine intensity based on adjusted score
        intensity = self._determine_intensity(primary_score)
        
        # Enhanced confidence calculation
        confidence = min(primary_score * 1.2, 0.95)  # Boost confidence and cap at 95%
        
        result = EmotionResult(
            primary_emotion=primary_emotion,
            confidence=confidence,
            secondary_emotions=secondary_emotions,
            emotional_intensity=intensity,
            context_keywords=context_keywords,
            timestamp=datetime.now()
        )
        
        self.logger.debug(f"Emotion detected: {primary_emotion} (confidence: {confidence:.2f})")
        return result

    def _calculate_emotion_score_fixed(self, text: str, patterns: Dict) -> float:
        """FIXED: Calculate emotion score with optimized algorithm"""
        score = 0.0
        base_weight = patterns.get('base_weight', 1.0)
        
        # Count keyword matches with higher base scores
        keyword_matches = 0
        keyword_score = 0.0
        
        for keyword in patterns['keywords']:
            if keyword in text:
                keyword_matches += 1
                base_score = 0.5 * base_weight  # Increased from 0.3 to 0.5
                
                # Apply intensity modifiers more aggressively
                for modifier, multiplier in patterns.get('intensity_modifiers', {}).items():
                    if modifier in text:
                        base_score *= multiplier
                        break
                
                keyword_score += base_score
        
        # Check regex patterns (even higher weight)
        pattern_score = 0.0
        for pattern in patterns.get('patterns', []):
            if re.search(pattern, text, re.IGNORECASE):
                pattern_score += 0.7 * base_weight  # Increased from 0.5 to 0.7
        
        # Combine scores
        total_score = keyword_score + pattern_score
        
        # Add bonus for multiple keyword matches
        if keyword_matches > 1:
            total_score *= (1.0 + (keyword_matches - 1) * 0.2)  # Bonus for multiple matches
        
        # Apply base weight multiplier
        total_score *= base_weight
        
        # Cap the score at reasonable level
        return min(total_score, 1.0)

    def _detect_context(self, text: str) -> List[str]:
        """Detect context categories in the text"""
        detected_contexts = []
        
        for category, keywords in self.context_categories.items():
            for keyword in keywords:
                if keyword in text:
                    if category not in detected_contexts:
                        detected_contexts.append(category)
                    break
        
        return detected_contexts

    def _determine_intensity(self, score: float) -> str:
        """Determine emotional intensity based on score with adjusted thresholds"""
        for intensity, (min_val, max_val) in self.intensity_thresholds.items():
            if min_val <= score < max_val:
                return intensity
        return 'high' if score >= 0.65 else 'medium'  # Default improved

    def _create_neutral_result(self, context_keywords: List[str] = None) -> EmotionResult:
        """Create a neutral emotion result"""
        return EmotionResult(
            primary_emotion='neutral',
            confidence=0.6,
            secondary_emotions=[],
            emotional_intensity='low',
            context_keywords=context_keywords or [],
            timestamp=datetime.now()
        )

    def get_emotion_summary(self, emotion_result: EmotionResult) -> str:
        """Get a human-readable summary of the emotion analysis"""
        summary = f"Primary: {emotion_result.primary_emotion.title()} "
        summary += f"({emotion_result.confidence:.0%} confidence, "
        summary += f"{emotion_result.emotional_intensity} intensity)"
        
        if emotion_result.secondary_emotions:
            secondary = ", ".join([f"{emo.title()}" for emo, _ in emotion_result.secondary_emotions[:2]])
            summary += f" | Secondary: {secondary}"
        
        if emotion_result.context_keywords:
            contexts = ", ".join([ctx.title() for ctx in emotion_result.context_keywords[:2]])
            summary += f" | Context: {contexts}"
        
        return summary

    def get_supported_emotions(self) -> List[str]:
        """Get list of all supported emotions"""
        return list(self.emotion_patterns.keys())

    def get_engine_stats(self) -> Dict:
        """Get engine statistics"""
        return {
            'supported_emotions': len(self.emotion_patterns),
            'emotion_types': list(self.emotion_patterns.keys()),
            'context_categories': len(self.context_categories),
            'total_keywords': sum(len(patterns['keywords']) for patterns in self.emotion_patterns.values()),
            'total_patterns': sum(len(patterns.get('patterns', [])) for patterns in self.emotion_patterns.values())
        }