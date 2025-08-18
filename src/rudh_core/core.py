# src\rudh_core\core.py
"""
Rudh AI Core - Compatible with Enhanced Emotion Detection Engine
Phase 2.1: Integration with 15+ emotion types and advanced confidence scoring
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
import json

# Import the enhanced emotion engine
from .emotion_engine import EnhancedEmotionEngine, EmotionResult

class RudhCore:
    """
    Enhanced Rudh AI Core with advanced emotion detection
    Phase 2.1: Upgraded emotional intelligence and response strategies
    """
    
    def __init__(self):
        """Initialize Rudh with enhanced capabilities"""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize enhanced emotion engine
        self.emotion_engine = EnhancedEmotionEngine()
        
        # Enhanced response strategies with emotion-specific handling
        self.response_strategies = {
            'emotional_support': {
                'triggers': ['joyful', 'sad', 'anxious', 'angry', 'fearful', 'lonely', 'guilty', 'disappointed'],
                'confidence_threshold': 0.3,
                'description': 'Providing empathetic emotional support and guidance'
            },
            'financial_advisor': {
                'triggers': ['investment', 'money', 'stock', 'financial', 'budget', 'wealth', 'advice', 'portfolio'],
                'confidence_threshold': 0.4,
                'description': 'Expert financial and investment guidance'
            },
            'creative_assistant': {
                'triggers': ['design', 'create', 'build', 'plan', 'develop', 'idea', 'project', 'creative'],
                'confidence_threshold': 0.4,
                'description': 'Creative problem-solving and design assistance'
            },
            'knowledge_sharing': {
                'triggers': ['what', 'how', 'why', 'explain', 'tell', 'learn', 'understand', 'know'],
                'confidence_threshold': 0.3,
                'description': 'Educational content and knowledge sharing'
            },
            'gratitude_response': {
                'triggers': ['grateful', 'surprised'],
                'confidence_threshold': 0.3,
                'description': 'Responding to gratitude and positive interactions'
            },
            'confusion_clarification': {
                'triggers': ['confused', 'unclear'],
                'confidence_threshold': 0.4,
                'description': 'Helping clarify confusing or unclear topics'
            },
            'celebration': {
                'triggers': ['excited', 'proud', 'hopeful'],
                'confidence_threshold': 0.4,
                'description': 'Celebrating achievements and positive moments'
            }
        }
        
        # Enhanced conversation memory with emotion tracking
        self.conversation_memory = []
        self.emotion_history = []
        self.max_memory_size = 100
        
        # Performance metrics
        self.stats = {
            'total_conversations': 0,
            'emotions_detected': {},
            'strategies_used': {},
            'average_confidence': 0.0,
            'session_start': datetime.now()
        }
        
        # Tamil responses with emotional context
        self.tamil_responses = {
            'joyful': [
                "மகிழ்ச்சி! உங்கள் சந்தோசம் என்னையும் மகிழ்வடையச் செய்கிறது! 🌟",
                "அருமை! உங்கள் மகிழ்ச்சியைப் பகிர்ந்துகொண்டதற்கு நன்றி!"
            ],
            'sad': [
                "வருத்தமாக இருக்கிறீர்களா? நான் உங்களுக்கு ஆறுதல் தர இருக்கிறேன். 💙",
                "கவலையில்லை, எல்லாம் சரியாகும். நான் உங்களுடன் இருக்கிறேன்."
            ],
            'anxious': [
                "கவலைப்படாதீர்கள். மூச்சு விடுங்கள். நான் உங்களுக்கு உதவுகிறேன். 🌸",
                "பதட்டம் இயல்பானது. ஒன்றும் பயப்படவேண்டாம்."
            ],
            'grateful': [
                "நன்றி! உங்கள் நன்றியுணர்வு என் மனதைத் தொடுகிறது! 🙏",
                "வரவேற்கிறேன்! எப்போதும் உதவ தயாராக இருக்கிறேன்."
            ],
            'general': [
                "வணக்கம்! எப்படி உதவ முடியும்?",
                "சொல்லுங்கள், என்ன உதவி வேண்டும்?"
            ]
        }
        
        self.logger.info("✅ Rudh Core Enhanced Edition initialized successfully")
        self.logger.info(f"🧠 Emotion Engine: {len(self.emotion_engine.get_supported_emotions())} emotions supported")

    def setup_logging(self):
        """Setup enhanced logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

    async def process_message(self, user_input: str, context: Optional[Dict] = None) -> Dict:
        """
        Enhanced message processing with advanced emotion detection
        
        Args:
            user_input: User's message
            context: Optional conversation context
            
        Returns:
            Comprehensive response package with emotion analysis
        """
        try:
            start_time = datetime.now()
            
            # Detect emotions using enhanced engine
            emotion_result = self.emotion_engine.detect_emotion(user_input, context)
            
            # Detect language
            language = self._detect_language(user_input)
            
            # Select response strategy based on emotion and content
            strategy, strategy_confidence = self._select_strategy(user_input, emotion_result)
            
            # Generate response
            response = await self._generate_response(
                user_input, emotion_result, strategy, language
            )
            
            # Update statistics
            self._update_statistics(emotion_result, strategy)
            
            # Store in memory
            self._store_conversation(user_input, response, emotion_result, strategy)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create comprehensive response package
            response_package = {
                'response': response,
                'emotion_analysis': {
                    'primary_emotion': emotion_result.primary_emotion,
                    'confidence': emotion_result.confidence,
                    'intensity': emotion_result.emotional_intensity,
                    'secondary_emotions': emotion_result.secondary_emotions,
                    'context': emotion_result.context_keywords,
                    'summary': self.emotion_engine.get_emotion_summary(emotion_result)
                },
                'strategy': {
                    'selected': strategy,
                    'confidence': strategy_confidence,
                    'description': self.response_strategies[strategy]['description']
                },
                'language': language,
                'processing_time': processing_time,
                'conversation_count': len(self.conversation_memory),
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Message processed: {emotion_result.primary_emotion} emotion, {strategy} strategy")
            
            return response_package
            
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {str(e)}")
            return self._create_error_response(str(e))

    def _select_strategy(self, user_input: str, emotion_result: EmotionResult) -> Tuple[str, float]:
        """
        Enhanced strategy selection based on emotion and content analysis
        """
        strategy_scores = {}
        text_lower = user_input.lower()
        
        # Check emotion-based triggers first (higher priority)
        for strategy, config in self.response_strategies.items():
            score = 0.0
            
            # Check if primary emotion triggers this strategy
            if emotion_result.primary_emotion in config['triggers']:
                score += 0.6 * emotion_result.confidence
            
            # Check if secondary emotions trigger this strategy
            for secondary_emotion, secondary_confidence in emotion_result.secondary_emotions:
                if secondary_emotion in config['triggers']:
                    score += 0.3 * secondary_confidence
            
            # Check keyword triggers
            keyword_matches = sum(1 for trigger in config['triggers'] 
                                if trigger in text_lower and trigger not in self.emotion_engine.get_supported_emotions())
            if keyword_matches > 0:
                score += 0.4 * (keyword_matches / len(config['triggers']))
            
            # Context boost
            for context in emotion_result.context_keywords:
                if context in ['work', 'money', 'financial'] and strategy == 'financial_advisor':
                    score += 0.2
                elif context in ['personal', 'family'] and strategy == 'emotional_support':
                    score += 0.2
            
            if score >= config['confidence_threshold']:
                strategy_scores[strategy] = score
        
        # Select strategy with highest score
        if strategy_scores:
            best_strategy = max(strategy_scores.items(), key=lambda x: x[1])
            return best_strategy[0], best_strategy[1]
        else:
            # Fallback to knowledge sharing
            return 'knowledge_sharing', 0.5

    async def _generate_response(self, user_input: str, emotion_result: EmotionResult, 
                               strategy: str, language: str) -> str:
        """Enhanced response generation with emotion-aware responses"""
        primary_emotion = emotion_result.primary_emotion
        intensity = emotion_result.emotional_intensity
        
        # Tamil language responses
        if language == 'tamil':
            if primary_emotion in self.tamil_responses:
                return self.tamil_responses[primary_emotion][0]
            else:
                return self.tamil_responses['general'][0]
        
        # English responses based on strategy and emotion
        if strategy == 'emotional_support':
            return self._generate_emotional_support_response(emotion_result, user_input)
        elif strategy == 'financial_advisor':
            return self._generate_financial_advice_response(emotion_result, user_input)
        elif strategy == 'creative_assistant':
            return self._generate_creative_response(emotion_result, user_input)
        elif strategy == 'gratitude_response':
            return self._generate_gratitude_response(emotion_result, user_input)
        elif strategy == 'confusion_clarification':
            return self._generate_clarification_response(emotion_result, user_input)
        elif strategy == 'celebration':
            return self._generate_celebration_response(emotion_result, user_input)
        else:  # knowledge_sharing
            return self._generate_knowledge_response(emotion_result, user_input)

    def _generate_emotional_support_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate empathetic emotional support responses"""
        emotion = emotion_result.primary_emotion
        intensity = emotion_result.emotional_intensity
        
        responses = {
            'sad': {
                'high': "I can sense you're going through a really difficult time right now. Your feelings are completely valid, and it's okay to feel this way. Remember that difficult emotions are temporary, and you have the strength to get through this. I'm here to support you. Would you like to talk about what's causing these feelings?",
                'medium': "I hear that you're feeling sad. It's natural to have these emotions sometimes. Take a moment to breathe and be gentle with yourself. What's one small thing that usually brings you a bit of comfort?",
                'low': "I notice you're feeling a bit down. That's completely normal - we all have those moments. Is there anything specific on your mind that you'd like to share?"
            },
            'anxious': {
                'high': "I can feel the anxiety in your words, and I want you to know that what you're experiencing is real and valid. Let's take this one step at a time. First, try taking three deep breaths with me. Anxiety can feel overwhelming, but you're stronger than you know. What's the main thing that's worrying you right now?",
                'medium': "It sounds like you're feeling stressed about something. Anxiety can be challenging, but remember that you've handled difficult situations before. What's one thing you can control in this situation?",
                'low': "I sense some worry in your message. Sometimes talking through our concerns can help put things in perspective. What's on your mind?"
            },
            'angry': {
                'high': "I can hear the frustration and anger in your words. These feelings are completely understandable - something has clearly upset you deeply. It's okay to feel angry; your emotions are valid. When you're ready, would you like to talk through what happened?",
                'medium': "It sounds like something has really frustrated you. Anger often signals that something important to us has been affected. What's the situation that's bothering you?",
                'low': "I sense some irritation in your message. Sometimes it helps to express what's bothering us. Would you like to share what's on your mind?"
            }
        }
        
        if emotion in responses and intensity in responses[emotion]:
            return responses[emotion][intensity]
        else:
            return f"I can sense you're experiencing {emotion} feelings. Your emotions are valid, and I'm here to support you. Would you like to share more about what you're going through?"

    def _generate_financial_advice_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate financial advice responses"""
        base_response = "I'd be happy to help with financial insights! "
        
        if 'anxious' in [emotion_result.primary_emotion] + [e[0] for e in emotion_result.secondary_emotions]:
            return base_response + "I understand financial decisions can feel stressful. Let's break this down step by step to make it more manageable. What specific area of finance are you most concerned about - investments, budgeting, savings, or something else?"
        
        return base_response + "I can assist with investment strategies, market analysis, portfolio planning, wealth building, and risk assessment. What specific financial area interests you most?"

    def _generate_creative_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate creative assistance responses"""
        if emotion_result.primary_emotion == 'excited':
            return "I love your enthusiasm for this creative project! That energy will fuel great results. Let's channel that excitement into something amazing. What kind of design or creative project are you working on?"
        
        return "I'm excited to help with your creative project! Whether it's design, planning, problem-solving, or brainstorming, I'm here to assist. What are you looking to create or develop?"

    def _generate_gratitude_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate responses to gratitude"""
        return "You're very welcome! Your gratitude truly brightens my day. I'm always here to help whenever you need assistance. Is there anything else I can support you with?"

    def _generate_clarification_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate clarification responses for confusion"""
        return "I can see this topic is causing some confusion, and that's completely understandable! I'm here to help clarify things. Let me break this down in a way that makes sense. What specific part would you like me to explain more clearly?"

    def _generate_celebration_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate celebratory responses for positive emotions"""
        emotion = emotion_result.primary_emotion
        
        if emotion == 'excited':
            return "Your excitement is contagious! I can feel your positive energy. This sounds like something wonderful is happening. Tell me more about what has you so thrilled!"
        
        if emotion == 'proud':
            return "You should absolutely feel proud! Achievement and personal growth deserve to be celebrated. Your hard work has paid off. What accomplishment are you most proud of?"
        
        return "I can sense your positive energy, and it's wonderful! Celebrating good moments is so important. What's bringing you joy today?"

    def _generate_knowledge_response(self, emotion_result: EmotionResult, user_input: str) -> str:
        """Generate knowledge-sharing responses"""
        return "I'm here to share knowledge and help you understand whatever you're curious about! Learning is one of life's greatest adventures. What topic interests you today?"

    def _detect_language(self, text: str) -> str:
        """Enhanced language detection with better Tamil recognition"""
        tamil_patterns = [
            r'[\u0B80-\u0BFF]',  # Tamil Unicode range
            r'\b(வணக்கம்|நன்றி|எப்படி|என்ன|எங்கள்|உங்கள்|நான்|அது|இது|அவர்|இவர்)\b'
        ]
        
        for pattern in tamil_patterns:
            if re.search(pattern, text):
                return 'tamil'
        
        return 'english'

    def _update_statistics(self, emotion_result: EmotionResult, strategy: str):
        """Update enhanced statistics tracking"""
        self.stats['total_conversations'] += 1
        
        # Track emotion frequency
        emotion = emotion_result.primary_emotion
        if emotion not in self.stats['emotions_detected']:
            self.stats['emotions_detected'][emotion] = 0
        self.stats['emotions_detected'][emotion] += 1
        
        # Track strategy usage
        if strategy not in self.stats['strategies_used']:
            self.stats['strategies_used'][strategy] = 0
        self.stats['strategies_used'][strategy] += 1
        
        # Update average confidence
        total_confidence = self.stats['average_confidence'] * (self.stats['total_conversations'] - 1)
        self.stats['average_confidence'] = (total_confidence + emotion_result.confidence) / self.stats['total_conversations']

    def _store_conversation(self, user_input: str, response: str, emotion_result: EmotionResult, strategy: str):
        """Enhanced conversation storage with emotion tracking"""
        conversation_entry = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'response': response,
            'emotion': emotion_result.primary_emotion,
            'emotion_confidence': emotion_result.confidence,
            'strategy': strategy,
            'context': emotion_result.context_keywords
        }
        
        self.conversation_memory.append(conversation_entry)
        self.emotion_history.append(emotion_result)
        
        # Maintain memory limit
        if len(self.conversation_memory) > self.max_memory_size:
            self.conversation_memory.pop(0)
        if len(self.emotion_history) > self.max_memory_size:
            self.emotion_history.pop(0)

    def get_enhanced_stats(self) -> Dict:
        """Get comprehensive statistics including emotion analysis"""
        runtime = (datetime.now() - self.stats['session_start']).total_seconds()
        
        return {
            'core_stats': self.stats,
            'emotion_engine_stats': self.emotion_engine.get_engine_stats(),
            'memory_usage': {
                'conversations_stored': len(self.conversation_memory),
                'emotions_tracked': len(self.emotion_history),
                'memory_limit': self.max_memory_size
            },
            'performance': {
                'session_runtime_seconds': runtime,
                'conversations_per_minute': (self.stats['total_conversations'] / runtime * 60) if runtime > 0 else 0
            },
            'recent_emotions': [e.primary_emotion for e in self.emotion_history[-10:]] if self.emotion_history else []
        }

    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history with emotion context"""
        recent_conversations = self.conversation_memory[-limit:] if self.conversation_memory else []
        
        formatted_history = []
        for conv in recent_conversations:
            formatted_history.append({
                'time': conv['timestamp'].strftime('%H:%M:%S'),
                'user': conv['user_input'][:100] + ('...' if len(conv['user_input']) > 100 else ''),
                'emotion': f"{conv['emotion'].title()} ({conv['emotion_confidence']:.0%})",
                'strategy': conv['strategy'].replace('_', ' ').title(),
                'context': ', '.join(conv['context']) if conv['context'] else 'None'
            })
        
        return formatted_history

    def _create_error_response(self, error_message: str) -> Dict:
        """Create standardized error response"""
        return {
            'response': "I apologize, but I encountered an issue processing your message. Let me try to help you in a different way. Could you please rephrase your question?",
            'emotion_analysis': {
                'primary_emotion': 'neutral',
                'confidence': 0.0,
                'intensity': 'low',
                'secondary_emotions': [],
                'context': [],
                'summary': 'Error in emotion detection'
            },
            'strategy': {
                'selected': 'knowledge_sharing',
                'confidence': 0.0,
                'description': 'Fallback error handling'
            },
            'language': 'english',
            'processing_time': 0.0,
            'conversation_count': len(self.conversation_memory),
            'timestamp': datetime.now().isoformat(),
            'error': error_message
        }