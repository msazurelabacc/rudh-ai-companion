"""
Rudh AI Advanced Context Engine - Phase 2.2
Context-aware response generation with multi-turn dialogue understanding
"""

import json
import time
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, deque
import re

@dataclass
class ConversationContext:
    """Represents conversation context state"""
    topic: str
    subtopics: List[str]
    user_goals: List[str]
    conversation_stage: str  # opening, building, deep_dive, closing
    urgency_level: str  # low, medium, high
    formality_level: str  # casual, professional, formal
    user_mood_trend: List[str]  # Recent mood progression
    key_entities: List[str]  # People, places, concepts mentioned
    user_preferences: Dict[str, float]  # Learned preferences with confidence
    
@dataclass
class ResponseStrategy:
    """Defines how to respond based on context"""
    strategy_type: str
    confidence: float
    reasoning: str
    tone_adjustments: Dict[str, float]
    content_focus: List[str]
    follow_up_suggestions: List[str]

class AdvancedContextEngine:
    """
    Advanced context understanding and response generation engine
    Provides multi-turn conversation awareness and intelligent response strategies
    """

    def _score_strategy(self, strategy_name: str, strategy_config: Dict,
                       context: ConversationContext, emotion_data: Dict) -> float:
        """Score how well a strategy fits the current context - OPTIMIZED"""
        score = 0.0
        
        # ENHANCED: Base score from emotion triggers (higher weight)
        if emotion_data and 'primary_emotion' in emotion_data:
            primary_emotion = emotion_data['primary_emotion']
            if primary_emotion in strategy_config.get('triggers', []):
                score += 0.6  # Increased from 0.4
        
        # ENHANCED: Emotion-strategy mapping for better selection
        emotion_strategy_fit = {
            'frustrated': {'supportive': 0.7, 'analytical': 0.3},
            'sad': {'supportive': 0.8, 'conversational': 0.2},
            'anxious': {'supportive': 0.7, 'analytical': 0.2},
            'angry': {'supportive': 0.6, 'analytical': 0.3},
            'grateful': {'conversational': 0.7, 'supportive': 0.3},
            'excited': {'motivational': 0.6, 'conversational': 0.4},
            'confused': {'educational': 0.7, 'analytical': 0.3},
            'curious': {'educational': 0.8, 'analytical': 0.2},
            'hopeful': {'motivational': 0.7, 'conversational': 0.3},
            'disappointed': {'supportive': 0.7, 'motivational': 0.3},
            'proud': {'conversational': 0.6, 'motivational': 0.4},
            'neutral': {'conversational': 0.5, 'analytical': 0.3}
        }
        
        if emotion_data and 'primary_emotion' in emotion_data:
            primary_emotion = emotion_data['primary_emotion']
            if primary_emotion in emotion_strategy_fit:
                emotion_fit = emotion_strategy_fit[primary_emotion].get(strategy_name, 0)
                score += emotion_fit
        
        # Score based on user goals (reduced weight)
        goal_alignment = {
            'supportive': ['emotional_support', 'problem_solving'],
            'analytical': ['decision_making', 'problem_solving', 'planning'],
            'motivational': ['planning', 'problem_solving'],
            'educational': ['learning', 'problem_solving'],
            'conversational': ['conversation']
        }
        
        strategy_goals = goal_alignment.get(strategy_name, [])
        goal_matches = len(set(context.user_goals) & set(strategy_goals))
        score += goal_matches * 0.15  # Reduced from 0.2
        
        # Urgency adjustment (reduced impact)
        urgency_preference = {
            'supportive': {'high': 0.2, 'medium': 0.15, 'low': 0.1},
            'analytical': {'high': 0.1, 'medium': 0.2, 'low': 0.15},
            'motivational': {'high': 0.1, 'medium': 0.2, 'low': 0.15}
        }
        
        if strategy_name in urgency_preference:
            score += urgency_preference[strategy_name].get(context.urgency_level, 0)
        
        # Topic relevance (reduced impact)
        topic_strategy_fit = {
            'work': {'analytical': 0.2, 'motivational': 0.15, 'supportive': 0.15},
            'relationships': {'supportive': 0.2, 'conversational': 0.15},
            'health': {'supportive': 0.2, 'analytical': 0.1},
            'finance': {'analytical': 0.3, 'educational': 0.15},
            'learning': {'educational': 0.3, 'motivational': 0.15},
            'general': {'conversational': 0.1, 'supportive': 0.1}  # Added general topic
        }
        
        if context.topic in topic_strategy_fit:
            score += topic_strategy_fit[context.topic].get(strategy_name, 0)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def __init__(self):
        self.conversation_history = deque(maxlen=50)  # Recent conversation
        self.user_profile = self._initialize_user_profile()
        self.topic_transitions = deque(maxlen=20)
        self.context_cache = {}
        self.learning_patterns = defaultdict(list)
        
        # Context classification patterns
        self.topic_patterns = {
            'work': {
                'keywords': ['job', 'work', 'office', 'boss', 'colleague', 'project', 'deadline', 
                           'meeting', 'career', 'salary', 'promotion', 'interview'],
                'patterns': [r'\b(at work|in office|my job|work related|professional)\b'],
                'urgency_indicators': ['urgent', 'deadline', 'crisis', 'emergency', 'asap']
            },
            'relationships': {
                'keywords': ['friend', 'family', 'partner', 'spouse', 'relationship', 'dating',
                           'parents', 'children', 'love', 'marriage', 'breakup', 'conflict'],
                'patterns': [r'\b(my friend|my partner|family member|relationship with)\b'],
                'urgency_indicators': ['fight', 'argument', 'breaking up', 'divorce', 'conflict']
            },
            'health': {
                'keywords': ['health', 'doctor', 'sick', 'pain', 'medicine', 'hospital',
                           'exercise', 'diet', 'sleep', 'stress', 'anxiety', 'depression'],
                'patterns': [r'\b(health issue|feeling sick|doctor visit|medical)\b'],
                'urgency_indicators': ['emergency', 'severe', 'unbearable', 'urgent care']
            },
            'finance': {
                'keywords': ['money', 'budget', 'investment', 'debt', 'savings', 'loan',
                           'stock', 'expense', 'income', 'financial', 'bank', 'credit'],
                'patterns': [r'\b(financial planning|money matters|investment advice)\b'],
                'urgency_indicators': ['debt crisis', 'bankruptcy', 'urgent payment']
            },
            'personal_growth': {
                'keywords': ['goal', 'dream', 'aspiration', 'learning', 'skill', 'hobby',
                           'achievement', 'success', 'improvement', 'development'],
                'patterns': [r'\b(personal goal|want to learn|trying to improve)\b'],
                'urgency_indicators': ['deadline approaching', 'time running out']
            },
            'technology': {
                'keywords': ['computer', 'software', 'app', 'AI', 'coding', 'programming',
                           'tech', 'digital', 'online', 'website', 'data'],
                'patterns': [r'\b(tech problem|software issue|coding help)\b'],
                'urgency_indicators': ['system down', 'critical bug', 'data loss']
            },
            'creative': {
                'keywords': ['art', 'music', 'writing', 'design', 'creative', 'painting',
                           'poetry', 'story', 'composition', 'artistic'],
                'patterns': [r'\b(creative project|artistic work|writing story)\b'],
                'urgency_indicators': ['deadline', 'competition', 'submission due']
            }
        }
        
        # Response strategies
        self.response_strategies = {
            'supportive': {
                'description': 'Provide emotional support and encouragement',
                'tone_adjustments': {'warmth': 0.9, 'empathy': 0.9, 'optimism': 0.7},
                'content_focus': ['validation', 'encouragement', 'practical_support'],
                'triggers': ['sad', 'anxious', 'stressed', 'overwhelmed', 'frustrated']
            },
            'analytical': {
                'description': 'Provide logical analysis and structured thinking',
                'tone_adjustments': {'clarity': 0.9, 'logic': 0.9, 'precision': 0.8},
                'content_focus': ['analysis', 'options', 'pros_cons', 'step_by_step'],
                'triggers': ['confused', 'complex_problem', 'decision_needed']
            },
            'motivational': {
                'description': 'Inspire action and maintain momentum',
                'tone_adjustments': {'energy': 0.9, 'confidence': 0.8, 'encouragement': 0.9},
                'content_focus': ['action_steps', 'goals', 'progress', 'achievement'],
                'triggers': ['goal_setting', 'motivation_needed', 'procrastination']
            },
            'educational': {
                'description': 'Provide knowledge and learning guidance',
                'tone_adjustments': {'clarity': 0.9, 'patience': 0.8, 'thoroughness': 0.9},
                'content_focus': ['explanation', 'examples', 'resources', 'practice'],
                'triggers': ['learning', 'explanation_needed', 'skill_development']
            },
            'conversational': {
                'description': 'Engage in natural, flowing conversation',
                'tone_adjustments': {'friendliness': 0.8, 'curiosity': 0.7, 'relatability': 0.8},
                'content_focus': ['questions', 'shared_experience', 'exploration'],
                'triggers': ['casual_chat', 'getting_to_know', 'social_interaction']
            }
        }
        
    def _initialize_user_profile(self) -> Dict:
        """Initialize user profile with default values"""
        return {
            'personality_indicators': {
                'analytical': 0.5,
                'emotional': 0.5,
                'practical': 0.5,
                'creative': 0.5,
                'social': 0.5
            },
            'communication_preferences': {
                'detail_level': 0.5,  # 0=brief, 1=detailed
                'formality': 0.3,     # 0=casual, 1=formal
                'directness': 0.5,    # 0=indirect, 1=direct
                'emoji_usage': 0.3,   # 0=none, 1=frequent
            },
            'topic_interests': defaultdict(float),
            'conversation_patterns': {
                'typical_session_length': 10,
                'preferred_response_length': 'medium',
                'question_asking_frequency': 0.3
            },
            'learning_style': {
                'examples_preferred': True,
                'step_by_step_preferred': True,
                'visual_learner': False,
                'prefers_summary': False
            }
        }
    
    def analyze_context(self, user_input: str, emotion_data: Dict, 
                       conversation_history: List[Dict]) -> ConversationContext:
        """
        Analyze the current conversation context
        """
        start_time = time.time()
        
        # Extract topic and subtopics
        topic, subtopics = self._extract_topics(user_input, conversation_history)
        
        # Detect user goals
        goals = self._detect_user_goals(user_input, conversation_history)
        
        # Determine conversation stage
        stage = self._determine_conversation_stage(conversation_history)
        
        # Assess urgency and formality
        urgency = self._assess_urgency(user_input, topic)
        formality = self._assess_formality(user_input, conversation_history)
        
        # Track mood progression
        mood_trend = self._track_mood_trend(emotion_data, conversation_history)
        
        # Extract key entities
        entities = self._extract_entities(user_input)
        
        # Get user preferences
        preferences = self._get_relevant_preferences(topic)
        
        context = ConversationContext(
            topic=topic,
            subtopics=subtopics,
            user_goals=goals,
            conversation_stage=stage,
            urgency_level=urgency,
            formality_level=formality,
            user_mood_trend=mood_trend,
            key_entities=entities,
            user_preferences=preferences
        )
        
        # Cache context for performance
        context_key = f"{topic}_{len(conversation_history)}"
        self.context_cache[context_key] = context
        
        # Log performance
        processing_time = time.time() - start_time
        logging.info(f"Context analysis completed in {processing_time:.3f}s")
        
        return context
    
    def generate_response_strategy(self, context: ConversationContext, 
                                 emotion_data: Dict) -> ResponseStrategy:
        """
        Generate optimal response strategy based on context and emotion
        """
        strategy_scores = {}
        
        # Score each strategy based on context and emotion
        for strategy_name, strategy_config in self.response_strategies.items():
            score = self._score_strategy(strategy_name, strategy_config, 
                                       context, emotion_data)
            strategy_scores[strategy_name] = score
        
        # Select best strategy
        best_strategy = max(strategy_scores.items(), key=lambda x: x[1])
        strategy_name, confidence = best_strategy
        strategy_config = self.response_strategies[strategy_name]
        
        # Generate reasoning
        reasoning = self._generate_strategy_reasoning(strategy_name, context, emotion_data)
        
        # Adjust tone based on context
        tone_adjustments = self._adjust_tone_for_context(
            strategy_config['tone_adjustments'], context)
        
        # Generate follow-up suggestions
        follow_ups = self._generate_follow_ups(context, strategy_name)
        
        return ResponseStrategy(
            strategy_type=strategy_name,
            confidence=confidence,
            reasoning=reasoning,
            tone_adjustments=tone_adjustments,
            content_focus=strategy_config['content_focus'],
            follow_up_suggestions=follow_ups
        )
    
    def _extract_topics(self, user_input: str, history: List[Dict]) -> Tuple[str, List[str]]:
        """Extract main topic and subtopics from input and history"""
        text = user_input.lower()
        topic_scores = {}
        
        # Score topics based on keywords and patterns
        for topic, config in self.topic_patterns.items():
            score = 0
            
            # Check keywords
            for keyword in config['keywords']:
                if keyword in text:
                    score += 1
            
            # Check patterns
            for pattern in config['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 2
            
            # Consider conversation history
            if history:
                recent_text = ' '.join([msg.get('content', '') for msg in history[-3:]])
                for keyword in config['keywords']:
                    if keyword in recent_text.lower():
                        score += 0.5
            
            topic_scores[topic] = score
        
        # Select primary topic
        if topic_scores and max(topic_scores.values()) > 0:
            primary_topic = max(topic_scores.items(), key=lambda x: x[1])[0]
        else:
            primary_topic = 'general'
        
        # Extract subtopics (topics with score > 0)
        subtopics = [topic for topic, score in topic_scores.items() 
                    if score > 0 and topic != primary_topic]
        
        return primary_topic, subtopics
    
    def _detect_user_goals(self, user_input: str, history: List[Dict]) -> List[str]:
        """Detect what the user is trying to achieve"""
        text = user_input.lower()
        goals = []
        
        # Goal detection patterns
        goal_patterns = {
            'seeking_advice': [r'\bwhat should i\b', r'\bshould i\b', r'\badvice\b', 
                             r'\bwhat would you\b', r'\brecommend\b'],
            'problem_solving': [r'\bhow to\b', r'\bhow can i\b', r'\bproblem with\b',
                              r'\bissue with\b', r'\btrouble\b'],
            'learning': [r'\blearn\b', r'\bunderstand\b', r'\bexplain\b', 
                        r'\bteach me\b', r'\bhow does\b'],
            'emotional_support': [r'\bfeeling\b', r'\bupset\b', r'\bstressed\b',
                                r'\bneed support\b', r'\bhelp me cope\b'],
            'planning': [r'\bplan\b', r'\bschedule\b', r'\borganize\b',
                        r'\bprepare for\b', r'\bstrategy\b'],
            'decision_making': [r'\bdecide\b', r'\bchoose\b', r'\boptions\b',
                              r'\bwhich one\b', r'\bcompare\b']
        }
        
        for goal, patterns in goal_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    goals.append(goal)
                    break
        
        return goals if goals else ['conversation']
    
    def _determine_conversation_stage(self, history: List[Dict]) -> str:
        """Determine what stage of conversation we're in"""
        if not history:
            return 'opening'
        elif len(history) < 3:
            return 'building'
        elif len(history) < 8:
            return 'deep_dive'
        else:
            return 'established'
    
    def _assess_urgency(self, user_input: str, topic: str) -> str:
        """Assess urgency level of the request"""
        text = user_input.lower()
        urgency_keywords = {
            'high': ['urgent', 'emergency', 'asap', 'immediately', 'crisis', 'critical'],
            'medium': ['soon', 'important', 'need help', 'worried', 'concerned'],
            'low': ['when you can', 'eventually', 'thinking about', 'wondering']
        }
        
        # Check for urgency keywords
        for level, keywords in urgency_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return level
        
        # Check topic-specific urgency indicators
        if topic in self.topic_patterns:
            for indicator in self.topic_patterns[topic].get('urgency_indicators', []):
                if indicator in text:
                    return 'high'
        
        return 'low'
    
    def _assess_formality(self, user_input: str, history: List[Dict]) -> str:
        """Assess desired formality level"""
        text = user_input.lower()
        
        formal_indicators = ['please', 'would you', 'could you', 'i would appreciate']
        casual_indicators = ["what's", "don't", "can't", "won't", 'hey', 'hi there']
        
        formal_score = sum(1 for indicator in formal_indicators if indicator in text)
        casual_score = sum(1 for indicator in casual_indicators if indicator in text)
        
        if formal_score > casual_score:
            return 'formal'
        elif casual_score > formal_score:
            return 'casual'
        else:
            return 'professional'
    
    def _track_mood_trend(self, emotion_data: Dict, history: List[Dict]) -> List[str]:
        """Track mood progression over recent conversation"""
        trend = []
        
        # Add current emotion
        if emotion_data and 'primary_emotion' in emotion_data:
            trend.append(emotion_data['primary_emotion'])
        
        # Look at recent history for emotion patterns
        for msg in history[-5:]:
            if 'emotion' in msg:
                trend.append(msg['emotion'])
        
        return trend[-5:]  # Keep last 5 moods
    
    def _extract_entities(self, user_input: str) -> List[str]:
        """Extract key entities (people, places, concepts)"""
        entities = []
        
        # Simple entity extraction patterns
        patterns = {
            'person': r'\b(my|a) (friend|colleague|boss|partner|spouse|doctor|teacher)\b',
            'place': r'\b(at|in|to) (work|home|school|hospital|office|gym)\b',
            'time': r'\b(today|tomorrow|yesterday|this week|next month)\b'
        }
        
        for entity_type, pattern in patterns.items():
            matches = re.findall(pattern, user_input.lower())
            entities.extend([match[1] if isinstance(match, tuple) else match 
                           for match in matches])
        
        return list(set(entities))
    
    def _get_relevant_preferences(self, topic: str) -> Dict[str, float]:
        """Get user preferences relevant to current topic"""
        preferences = {}
        
        # Topic interest level
        if topic in self.user_profile['topic_interests']:
            preferences['topic_interest'] = self.user_profile['topic_interests'][topic]
        
        # Communication preferences
        preferences.update(self.user_profile['communication_preferences'])
        
        return preferences
    
    def _generate_strategy_reasoning(self, strategy_name: str, 
                                   context: ConversationContext, 
                                   emotion_data: Dict) -> str:
        """Generate explanation for why this strategy was chosen"""
        reasons = []
        
        if emotion_data and 'primary_emotion' in emotion_data:
            emotion = emotion_data['primary_emotion']
            reasons.append(f"User shows {emotion} emotion")
        
        if context.user_goals:
            goals_text = ', '.join(context.user_goals)
            reasons.append(f"Goals detected: {goals_text}")
        
        reasons.append(f"Topic: {context.topic}")
        reasons.append(f"Urgency: {context.urgency_level}")
        
        return f"Selected {strategy_name} strategy based on: " + "; ".join(reasons)
    
    def _adjust_tone_for_context(self, base_tone: Dict[str, float], 
                                context: ConversationContext) -> Dict[str, float]:
        """Adjust tone based on conversation context"""
        adjusted_tone = base_tone.copy()
        
        # Adjust for formality
        if context.formality_level == 'formal':
            adjusted_tone['professionalism'] = adjusted_tone.get('professionalism', 0.5) + 0.2
        elif context.formality_level == 'casual':
            adjusted_tone['friendliness'] = adjusted_tone.get('friendliness', 0.5) + 0.2
        
        # Adjust for urgency
        if context.urgency_level == 'high':
            adjusted_tone['responsiveness'] = adjusted_tone.get('responsiveness', 0.5) + 0.3
            adjusted_tone['clarity'] = adjusted_tone.get('clarity', 0.5) + 0.2
        
        # Adjust for mood trend
        if context.user_mood_trend:
            recent_moods = context.user_mood_trend[-3:]
            if 'sad' in recent_moods or 'anxious' in recent_moods:
                adjusted_tone['empathy'] = adjusted_tone.get('empathy', 0.5) + 0.2
                adjusted_tone['warmth'] = adjusted_tone.get('warmth', 0.5) + 0.2
        
        # Normalize values to [0, 1]
        for key, value in adjusted_tone.items():
            adjusted_tone[key] = min(max(value, 0.0), 1.0)
        
        return adjusted_tone
    
    def _generate_follow_ups(self, context: ConversationContext, 
                           strategy_name: str) -> List[str]:
        """Generate contextual follow-up suggestions"""
        follow_ups = []
        
        # Strategy-specific follow-ups
        strategy_follow_ups = {
            'supportive': [
                "Would you like to talk more about how you're feeling?",
                "Is there anything specific that would help you feel better?",
                "How can I best support you through this?"
            ],
            'analytical': [
                "Would you like me to break this down into smaller steps?",
                "Should we explore the pros and cons of each option?",
                "What additional information would be helpful?"
            ],
            'motivational': [
                "What's your next step going to be?",
                "How can we track your progress on this?",
                "What would success look like for you?"
            ],
            'educational': [
                "Would you like me to explain any part in more detail?",
                "Are there related topics you'd like to explore?",
                "Would examples help clarify this concept?"
            ],
            'conversational': [
                "What's your take on this?",
                "How does this relate to your experience?",
                "What aspects interest you most?"
            ]
        }
        
        base_follow_ups = strategy_follow_ups.get(strategy_name, [])
        
        # Add context-specific follow-ups
        if context.topic == 'work' and 'problem_solving' in context.user_goals:
            follow_ups.append("Would discussing this with your colleagues be helpful?")
        
        if context.urgency_level == 'high':
            follow_ups.append("Is this something that needs immediate action?")
        
        # Select up to 3 most relevant follow-ups
        return (base_follow_ups + follow_ups)[:3]
    
    def update_user_profile(self, user_input: str, context: ConversationContext, 
                          response_feedback: Optional[Dict] = None):
        """Update user profile based on interaction"""
        # Update topic interests
        self.user_profile['topic_interests'][context.topic] += 0.1
        
        # Update communication preferences based on input style
        input_length = len(user_input.split())
        if input_length > 20:
            self.user_profile['communication_preferences']['detail_level'] += 0.05
        elif input_length < 5:
            self.user_profile['communication_preferences']['detail_level'] -= 0.05
        
        # Update personality indicators based on goals and topics
        if 'analytical' in context.user_goals or context.topic in ['finance', 'work']:
            self.user_profile['personality_indicators']['analytical'] += 0.02
        
        if 'emotional_support' in context.user_goals:
            self.user_profile['personality_indicators']['emotional'] += 0.02
        
        # Normalize values
        for category in ['personality_indicators', 'communication_preferences']:
            for key, value in self.user_profile[category].items():
                self.user_profile[category][key] = min(max(value, 0.0), 1.0)
    
    def get_context_summary(self, context: ConversationContext) -> Dict[str, Any]:
        """Get a summary of current context for display"""
        return {
            'primary_topic': context.topic,
            'conversation_stage': context.conversation_stage,
            'user_goals': context.user_goals,
            'urgency_level': context.urgency_level,
            'formality_level': context.formality_level,
            'key_entities': context.key_entities,
            'mood_trend': context.user_mood_trend[-3:] if context.user_mood_trend else [],
            'preferences_applied': len(context.user_preferences)
        }
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics about context engine performance"""
        return {
            'total_contexts_analyzed': len(self.context_cache),
            'user_profile_maturity': {
                'topic_interests': len(self.user_profile['topic_interests']),
                'personality_confidence': sum(self.user_profile['personality_indicators'].values()) / 5,
                'communication_preferences_learned': len([v for v in self.user_profile['communication_preferences'].values() if v != 0.5])
            },
            'conversation_patterns': {
                'average_session_length': self.user_profile['conversation_patterns']['typical_session_length'],
                'topic_distribution': dict(self.user_profile['topic_interests']),
                'mood_patterns': list(self.learning_patterns.keys()) if self.learning_patterns else []
            }
        }

# Example usage and testing
if __name__ == "__main__":
    print("🧠 Advanced Context Engine - Phase 2.2")
    print("="*50)
    
    # Initialize context engine
    context_engine = AdvancedContextEngine()
    
    # Test context analysis
    test_cases = [
        {
            'input': "I'm having trouble with a work project and feeling stressed about the deadline",
            'emotion': {'primary_emotion': 'anxious', 'confidence': 0.8, 'intensity': 'high'},
            'history': []
        },
        {
            'input': "Can you help me understand how to invest in stocks?",
            'emotion': {'primary_emotion': 'curious', 'confidence': 0.7, 'intensity': 'medium'},
            'history': [{'content': 'talking about financial planning', 'timestamp': datetime.now()}]
        },
        {
            'input': "Thank you for the advice, that really helped!",
            'emotion': {'primary_emotion': 'grateful', 'confidence': 0.9, 'intensity': 'high'},
            'history': [
                {'content': 'investment advice discussion', 'timestamp': datetime.now()},
                {'content': 'explained portfolio diversification', 'timestamp': datetime.now()}
            ]
        }
    ]
    
    print("\n🧪 Testing Context Analysis:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['input'][:50]}...")
        
        start_time = time.time()
        context = context_engine.analyze_context(
            test_case['input'], 
            test_case['emotion'], 
            test_case['history']
        )
        
        strategy = context_engine.generate_response_strategy(context, test_case['emotion'])
        
        processing_time = time.time() - start_time
        
        print(f"✅ Context Analysis ({processing_time:.3f}s):")
        print(f"   Topic: {context.topic}")
        print(f"   Goals: {', '.join(context.user_goals)}")
        print(f"   Stage: {context.conversation_stage}")
        print(f"   Urgency: {context.urgency_level}")
        print(f"   Formality: {context.formality_level}")
        
        print(f"✅ Response Strategy ({strategy.confidence:.1%} confidence):")
        print(f"   Strategy: {strategy.strategy_type}")
        print(f"   Reasoning: {strategy.reasoning}")
        print(f"   Focus: {', '.join(strategy.content_focus)}")
        
        # Update user profile
        context_engine.update_user_profile(test_case['input'], context)
    
    print(f"\n📊 Context Engine Analytics:")
    analytics = context_engine.get_analytics()
    
    print(f"   Contexts Analyzed: {analytics['total_contexts_analyzed']}")
    print(f"   User Profile Maturity: {analytics['user_profile_maturity']['personality_confidence']:.1%}")
    print(f"   Topics Learned: {analytics['user_profile_maturity']['topic_interests']}")
    print(f"   Communication Preferences: {analytics['user_profile_maturity']['communication_preferences_learned']}")
    
    print("\n🎉 Advanced Context Engine Test Complete!")
    print("Ready for integration with Rudh Core!")