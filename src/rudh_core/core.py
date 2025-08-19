"""
Enhanced Rudh Core - Phase 2.2 COMPLETE
Integrated emotion detection and advanced context awareness
"""

import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict

# Import our enhanced engines
from .emotion_engine import EnhancedEmotionEngine
from .context_engine import AdvancedContextEngine

class EnhancedRudhCore:
    """
    Enhanced Rudh AI Core with advanced emotion detection and context awareness
    Phase 2.2: Context-aware response generation
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize enhanced Rudh core with emotion and context engines"""
        self.config = config or {}
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI engines
        self.emotion_engine = EnhancedEmotionEngine()
        self.context_engine = AdvancedContextEngine()
        
        # Conversation management
        self.conversation_history = []
        self.session_stats = {
            'messages_processed': 0,
            'total_processing_time': 0,
            'average_confidence': 0,
            'emotions_detected': {},
            'topics_discussed': {},
            'strategies_used': {},
            'session_start': datetime.now()
        }
        
        # Response templates enhanced with context awareness
        self.response_templates = {
            'supportive': {
                'casual': [
                    "I can really understand how {emotion} you must be feeling about {topic}. {empathy_response}",
                    "That sounds {intensity} {emotion}. {validation} {support_offer}",
                    "I hear you - dealing with {topic} can be really {emotion}. {encouragement}"
                ],
                'professional': [
                    "I understand this {topic} situation is causing you to feel {emotion}. {professional_support}",
                    "Your {emotion} feelings about {topic} are completely valid. {structured_support}",
                    "I recognize the {intensity} {emotion} you're experiencing with {topic}. {professional_guidance}"
                ],
                'formal': [
                    "I acknowledge your {emotion} feelings regarding {topic}. {formal_support}",
                    "Your emotional response to {topic} is understandable. {formal_guidance}",
                    "I recognize the significance of your {emotion} experience with {topic}. {formal_assistance}"
                ]
            },
            'analytical': {
                'casual': [
                    "Let's break down this {topic} situation. {analysis_intro} {logical_steps}",
                    "Looking at your {topic} challenge, here's what I'm thinking: {analytical_response}",
                    "So with {topic}, we've got a few things to consider: {options_list}"
                ],
                'professional': [
                    "Analyzing your {topic} situation, I can identify several key factors: {professional_analysis}",
                    "From a strategic perspective on {topic}: {structured_analysis}",
                    "Considering the {topic} context, here's my assessment: {professional_breakdown}"
                ],
                'formal': [
                    "Upon analysis of your {topic} inquiry, the following considerations emerge: {formal_analysis}",
                    "A systematic evaluation of {topic} reveals: {formal_assessment}",
                    "The {topic} situation presents these analytical points: {formal_breakdown}"
                ]
            },
            'educational': {
                'casual': [
                    "Great question about {topic}! Let me explain it this way: {simple_explanation}",
                    "So you want to learn about {topic}? Here's the deal: {engaging_explanation}",
                    "I love that you're curious about {topic}! {enthusiastic_teaching}"
                ],
                'professional': [
                    "I'm happy to explain {topic}. {professional_introduction} {structured_explanation}",
                    "Regarding your question about {topic}: {professional_teaching}",
                    "To help you understand {topic} better: {comprehensive_explanation}"
                ],
                'formal': [
                    "In response to your inquiry about {topic}: {formal_explanation}",
                    "To provide clarity on {topic}: {academic_explanation}",
                    "Regarding the {topic} concept you've asked about: {formal_teaching}"
                ]
            },
            'motivational': {
                'casual': [
                    "You've got this! {topic} might seem tough, but {encouragement} {action_steps}",
                    "I believe in you with {topic}! {motivation} {next_steps}",
                    "Let's make {topic} happen! {energy} {goal_alignment}"
                ],
                'professional': [
                    "You have the capability to succeed with {topic}. {professional_motivation} {strategic_steps}",
                    "Your goals regarding {topic} are achievable. {structured_encouragement} {action_plan}",
                    "Success in {topic} is within your reach. {professional_empowerment} {guidance}"
                ],
                'formal': [
                    "Your objectives concerning {topic} are attainable. {formal_encouragement} {structured_approach}",
                    "Achievement in {topic} is certainly possible. {formal_motivation} {systematic_guidance}",
                    "Your aspirations regarding {topic} can be realized. {formal_empowerment} {methodical_steps}"
                ]
            },
            'conversational': {
                'casual': [
                    "That's interesting about {topic}! {conversational_response} {follow_up_question}",
                    "Oh, {topic}! {relatable_response} {engaging_continuation}",
                    "I find {topic} fascinating too! {shared_interest} {exploration}"
                ],
                'professional': [
                    "Thank you for sharing about {topic}. {professional_engagement} {thoughtful_response}",
                    "Your perspective on {topic} is valuable. {professional_conversation} {meaningful_exchange}",
                    "I appreciate your thoughts on {topic}. {professional_dialogue} {continued_discussion}"
                ],
                'formal': [
                    "Your observations regarding {topic} are noteworthy. {formal_acknowledgment} {respectful_dialogue}",
                    "I find your perspective on {topic} quite insightful. {formal_engagement} {scholarly_discussion}",
                    "Your viewpoint concerning {topic} merits consideration. {formal_conversation} {intellectual_exchange}"
                ]
            }
        }
        
        # Context-specific response elements
        self.response_elements = {
            'empathy_response': {
                'high_emotion': "That must be really overwhelming for you.",
                'medium_emotion': "I can imagine that's quite challenging.",
                'low_emotion': "That sounds like something worth talking about."
            },
            'validation': {
                'work': "Work stress is incredibly common and your feelings are completely valid.",
                'relationships': "Relationship challenges affect us deeply, and it's natural to feel this way.",
                'health': "Health concerns can be very worrying, and your feelings make complete sense.",
                'finance': "Financial matters can be really stressful, and your concerns are understandable."
            },
            'support_offer': {
                'high_urgency': "What would be most helpful for you right now?",
                'medium_urgency': "How can I best support you through this?",
                'low_urgency': "I'm here to help you work through this when you're ready."
            },
            'encouragement': {
                'general': "You're not alone in this, and there are ways to move forward.",
                'specific': "Your awareness of this situation is already a positive step forward."
            }
        }
        
        self.logger.info("Enhanced Rudh Core initialized with emotion and context engines")
    
    async def process_message(self, user_input: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process user message with enhanced emotion detection and context awareness
        """
        start_time = time.time()
        
        try:
            # Phase 1: Emotion Analysis
            emotion_start = time.time()
            emotion_result = await self.emotion_engine.analyze_emotion(user_input)
            emotion_time = time.time() - emotion_start
            
            # Phase 2: Context Analysis  
            context_start = time.time()
            conversation_context = self.context_engine.analyze_context(
                user_input, 
                emotion_result, 
                self.conversation_history[-10:]  # Last 10 messages for context
            )
            context_time = time.time() - context_start
            
            # Phase 3: Response Strategy Generation
            strategy_start = time.time()
            response_strategy = self.context_engine.generate_response_strategy(
                conversation_context, 
                emotion_result
            )
            strategy_time = time.time() - strategy_start
            
            # Phase 4: Enhanced Response Generation
            response_start = time.time()
            response_content = await self._generate_contextual_response(
                user_input, 
                emotion_result, 
                conversation_context, 
                response_strategy
            )
            response_time = time.time() - response_start
            
            # Phase 5: Update User Profile and Memory
            memory_start = time.time()
            self.context_engine.update_user_profile(user_input, conversation_context)
            self._update_conversation_memory(user_input, emotion_result, conversation_context, response_content)
            memory_time = time.time() - memory_start
            
            # Calculate total processing time
            total_time = time.time() - start_time
            
            # Update session statistics
            self._update_session_stats(emotion_result, conversation_context, response_strategy, total_time)
            
            # Prepare comprehensive response
            enhanced_response = {
                'response': response_content,
                'emotion_analysis': {
                    'primary_emotion': emotion_result.get('primary_emotion', 'neutral'),
                    'confidence': emotion_result.get('confidence', 0.0),
                    'intensity': emotion_result.get('intensity', 'medium'),
                    'secondary_emotions': emotion_result.get('secondary_emotions', []),
                    'processing_time': f"{emotion_time:.3f}s"
                },
                'context_analysis': {
                    'topic': conversation_context.topic,
                    'conversation_stage': conversation_context.conversation_stage,
                    'user_goals': conversation_context.user_goals,
                    'urgency_level': conversation_context.urgency_level,
                    'formality_level': conversation_context.formality_level,
                    'key_entities': conversation_context.key_entities,
                    'mood_trend': conversation_context.user_mood_trend,
                    'processing_time': f"{context_time:.3f}s"
                },
                'response_strategy': {
                    'strategy_type': response_strategy.strategy_type,
                    'confidence': response_strategy.confidence,
                    'reasoning': response_strategy.reasoning,
                    'content_focus': response_strategy.content_focus,
                    'follow_up_suggestions': response_strategy.follow_up_suggestions,
                    'processing_time': f"{strategy_time:.3f}s"
                },
                'performance_metrics': {
                    'total_processing_time': f"{total_time:.3f}s",
                    'emotion_processing': f"{emotion_time:.3f}s",
                    'context_processing': f"{context_time:.3f}s",
                    'strategy_processing': f"{strategy_time:.3f}s",
                    'response_generation': f"{response_time:.3f}s",
                    'memory_update': f"{memory_time:.3f}s"
                },
                'session_info': {
                    'message_count': self.session_stats['messages_processed'],
                    'session_duration': str(datetime.now() - self.session_stats['session_start']).split('.')[0],
                    'average_confidence': f"{self.session_stats['average_confidence']:.1f}%"
                }
            }
            
            self.logger.info(f"Message processed successfully in {total_time:.3f}s")
            return enhanced_response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return {
                'response': "I apologize, but I encountered an error processing your message. Please try again.",
                'error': str(e),
                'processing_time': f"{time.time() - start_time:.3f}s"
            }
    
    async def _generate_contextual_response(self, user_input: str, emotion_result: Dict,
                                          conversation_context, response_strategy) -> str:
        """
        Generate contextually appropriate response using templates and strategies
        """
        try:
            # Get base template based on strategy and formality
            strategy_type = response_strategy.strategy_type
            formality = conversation_context.formality_level
            
            templates = self.response_templates.get(strategy_type, {}).get(formality, [])
            if not templates:
                templates = self.response_templates['conversational']['casual']
            
            # Select template based on context
            template = self._select_best_template(templates, conversation_context, emotion_result)
            
            # Prepare template variables
            template_vars = {
                'emotion': emotion_result.get('primary_emotion', 'uncertain'),
                'intensity': emotion_result.get('intensity', 'medium'),
                'topic': conversation_context.topic,
                'urgency': conversation_context.urgency_level
            }
            
            # Add context-specific response elements
            template_vars.update(self._get_response_elements(conversation_context, emotion_result))
            
            # Format template with variables
            try:
                formatted_response = template.format(**template_vars)
            except KeyError as e:
                # Fallback if template formatting fails
                self.logger.warning(f"Template formatting failed: {e}")
                formatted_response = self._generate_fallback_response(conversation_context, emotion_result)
            
            # Add strategy-specific enhancements
            enhanced_response = self._enhance_response_with_strategy(
                formatted_response, response_strategy, conversation_context
            )
            
            # Add follow-up suggestions if appropriate
            if response_strategy.follow_up_suggestions and len(response_strategy.follow_up_suggestions) > 0:
                follow_up = response_strategy.follow_up_suggestions[0]  # Use first suggestion
                enhanced_response += f"\n\n{follow_up}"
            
            return enhanced_response
            
        except Exception as e:
            self.logger.error(f"Error generating contextual response: {e}")
            return self._generate_fallback_response(conversation_context, emotion_result)
    
    def _select_best_template(self, templates: List[str], context, emotion_result: Dict) -> str:
        """Select the most appropriate template based on context"""
        if not templates:
            return "I understand you're feeling {emotion} about {topic}. How can I help you with this?"
        
        # For now, select based on conversation stage
        if context.conversation_stage == 'opening':
            return templates[0] if len(templates) > 0 else templates[0]
        elif context.conversation_stage == 'deep_dive':
            return templates[-1] if len(templates) > 1 else templates[0]
        else:
            return templates[len(templates)//2] if len(templates) > 2 else templates[0]
    
    def _get_response_elements(self, context, emotion_result: Dict) -> Dict[str, str]:
        """Get context-specific response elements"""
        elements = {}
        
        # Empathy response based on emotion intensity
        intensity = emotion_result.get('intensity', 'medium')
        empathy_key = f"{intensity}_emotion"
        elements['empathy_response'] = self.response_elements['empathy_response'].get(
            empathy_key, self.response_elements['empathy_response']['medium_emotion']
        )
        
        # Validation based on topic
        elements['validation'] = self.response_elements['validation'].get(
            context.topic, "Your feelings about this are completely understandable."
        )
        
        # Support offer based on urgency
        urgency_key = f"{context.urgency_level}_urgency"
        elements['support_offer'] = self.response_elements['support_offer'].get(
            urgency_key, self.response_elements['support_offer']['medium_urgency']
        )
        
        # Encouragement
        elements['encouragement'] = self.response_elements['encouragement']['general']
        
        # ADD ALL MISSING TEMPLATE ELEMENTS:
        
        # Analysis elements
        elements['analysis_intro'] = "Looking at this situation,"
        elements['logical_steps'] = "here are the key factors to consider."
        elements['analytical_response'] = "I can help you analyze this systematically."
        elements['options_list'] = "Let's explore your available options."
        elements['pros_cons'] = "We can weigh the advantages and disadvantages."
        elements['step_by_step'] = "I'll break this down step by step."
        
        # Professional analysis elements
        elements['professional_analysis'] = "From a strategic perspective, here's my assessment."
        elements['structured_analysis'] = "Let me provide a systematic evaluation."
        elements['professional_breakdown'] = "Here's a comprehensive analysis."
        elements['professional_assessment'] = "My professional evaluation suggests:"
        elements['structured_support'] = "Let me provide structured support for this."
        elements['professional_guidance'] = "Here's my professional guidance on this matter."
        
        # Formal analysis elements  
        elements['formal_analysis'] = "Upon careful consideration, the following points emerge."
        elements['formal_assessment'] = "A thorough evaluation reveals:"
        elements['formal_breakdown'] = "The systematic analysis indicates:"
        elements['formal_support'] = "I offer my formal support in this matter."
        elements['formal_guidance'] = "Allow me to provide formal guidance."
        elements['formal_assistance'] = "I shall provide formal assistance."
        
        # Educational elements
        elements['simple_explanation'] = "Let me explain this clearly."
        elements['engaging_explanation'] = "Here's how this works."
        elements['enthusiastic_teaching'] = "I'm excited to help you learn this!"
        elements['professional_introduction'] = "To help you understand this better:"
        elements['structured_explanation'] = "Let me break this down systematically."
        elements['professional_teaching'] = "Here's a comprehensive explanation."
        elements['comprehensive_explanation'] = "I'll provide a detailed overview."
        elements['formal_explanation'] = "Allow me to elucidate this concept."
        elements['academic_explanation'] = "From an educational standpoint:"
        elements['formal_teaching'] = "I shall explain this systematically."
        
        # Motivational elements
        elements['motivation'] = "I believe in your capacity to succeed."
        elements['next_steps'] = "Here's what you can do moving forward."
        elements['action_steps'] = "Consider taking these practical steps."
        elements['goal_alignment'] = "Let's align this with your objectives."
        elements['energy'] = "You've got the energy to make this happen!"
        elements['professional_motivation'] = "You have the skills to achieve this."
        elements['structured_encouragement'] = "Success is within your reach."
        elements['action_plan'] = "Here's a strategic action plan."
        elements['professional_empowerment'] = "You're capable of handling this."
        elements['guidance'] = "I'll guide you through this process."
        elements['formal_encouragement'] = "Your success is entirely achievable."
        elements['formal_motivation'] = "You possess the necessary capabilities."
        elements['systematic_guidance'] = "Follow this systematic approach."
        elements['formal_empowerment'] = "You are well-equipped to succeed."
        elements['methodical_steps'] = "These methodical steps will help."
        elements['strategic_steps'] = "Here are strategic steps to consider."
        elements['structured_approach'] = "A structured approach will serve you well."
        
        # Conversational elements
        elements['conversational_response'] = "That's really interesting!"
        elements['follow_up_question'] = "What's your take on this?"
        elements['relatable_response'] = "I can relate to that perspective."
        elements['engaging_continuation'] = "Tell me more about your thoughts."
        elements['shared_interest'] = "I find this topic fascinating too."
        elements['exploration'] = "Let's explore this together."
        elements['professional_engagement'] = "I appreciate your perspective on this."
        elements['thoughtful_response'] = "That's a thoughtful observation."
        elements['professional_conversation'] = "Your insights are valuable."
        elements['meaningful_exchange'] = "This is a meaningful discussion."
        elements['professional_dialogue'] = "I value this professional dialogue."
        elements['continued_discussion'] = "Let's continue this conversation."
        elements['formal_acknowledgment'] = "I acknowledge your viewpoint."
        elements['respectful_dialogue'] = "This is a respectful exchange."
        elements['formal_engagement'] = "I appreciate your engagement."
        elements['scholarly_discussion'] = "This scholarly discussion is valuable."
        elements['formal_conversation'] = "I value this formal discourse."
        elements['intellectual_exchange'] = "This intellectual exchange is enriching."
        
        # Strategy-specific elements based on topic
        if context.topic == 'work':
            elements['professional_support'] = "Let's work through this professional challenge together."
            elements['analysis_intro'] = "From a work perspective,"
            elements['action_steps'] = "Here are some practical steps you can take:"
        elif context.topic == 'relationships':
            elements['professional_support'] = "Relationship challenges can be complex to navigate."
            elements['analysis_intro'] = "Looking at this relationship situation,"
            elements['action_steps'] = "Consider these approaches:"
        elif context.topic == 'finance':
            elements['professional_support'] = "Financial decisions can have lasting impact."
            elements['analysis_intro'] = "From a financial planning perspective,"
            elements['action_steps'] = "Here are some financial strategies:"
        else:
            elements['professional_support'] = "I'm here to support you through this."
            elements['analysis_intro'] = "Looking at this situation,"
            elements['action_steps'] = "Here are some steps to consider:"
        
        return elements
    
    def _enhance_response_with_strategy(self, base_response: str, strategy, context) -> str:
        """Enhance response based on selected strategy"""
        enhancements = []
        
        if strategy.strategy_type == 'analytical':
            if 'analysis' in strategy.content_focus:
                enhancements.append("Let me break this down systematically for you.")
            if 'options' in strategy.content_focus:
                enhancements.append("Here are the key options to consider:")
        
        elif strategy.strategy_type == 'supportive':
            if 'validation' in strategy.content_focus:
                enhancements.append("Your feelings are completely valid and understandable.")
            if 'encouragement' in strategy.content_focus:
                enhancements.append("Remember, you have the strength to get through this.")
        
        elif strategy.strategy_type == 'motivational':
            if 'action_steps' in strategy.content_focus:
                enhancements.append("The important thing is taking that first step forward.")
            if 'goals' in strategy.content_focus:
                enhancements.append("Your goals are achievable with the right approach.")
        
        elif strategy.strategy_type == 'educational':
            if 'explanation' in strategy.content_focus:
                enhancements.append("I'll explain this in a way that's easy to understand.")
            if 'examples' in strategy.content_focus:
                enhancements.append("Let me give you some concrete examples.")
        
        # Add enhancements to response
        if enhancements:
            enhanced = base_response + " " + " ".join(enhancements)
            return enhanced
        
        return base_response
    
    def _generate_fallback_response(self, context, emotion_result: Dict) -> str:
        """Generate a safe fallback response"""
        emotion = emotion_result.get('primary_emotion', 'uncertain')
        topic = context.topic if hasattr(context, 'topic') else 'this situation'
        
        return f"I understand you're feeling {emotion} about {topic}. I'm here to help you work through this. What would be most helpful for you right now?"
    
    def _update_conversation_memory(self, user_input: str, emotion_result: Dict, 
                                  context, response_content: str):
        """Update conversation memory with enhanced context"""
        memory_entry = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'emotion': emotion_result.get('primary_emotion', 'neutral'),
            'emotion_confidence': emotion_result.get('confidence', 0.0),
            'topic': context.topic,
            'user_goals': context.user_goals,
            'conversation_stage': context.conversation_stage,
            'urgency': context.urgency_level,
            'formality': context.formality_level,
            'response': response_content,
            'strategy_used': getattr(context, 'strategy_type', 'unknown')
        }
        
        self.conversation_history.append(memory_entry)
        
        # Keep memory manageable (last 100 entries)
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
    
    def _update_session_stats(self, emotion_result: Dict, context, strategy, processing_time: float):
        """Update session statistics"""
        self.session_stats['messages_processed'] += 1
        self.session_stats['total_processing_time'] += processing_time
        
        # Update emotion statistics
        emotion = emotion_result.get('primary_emotion', 'neutral')
        self.session_stats['emotions_detected'][emotion] = \
            self.session_stats['emotions_detected'].get(emotion, 0) + 1
        
        # Update topic statistics
        topic = context.topic
        self.session_stats['topics_discussed'][topic] = \
            self.session_stats['topics_discussed'].get(topic, 0) + 1
        
        # Update strategy statistics
        strategy_type = strategy.strategy_type
        self.session_stats['strategies_used'][strategy_type] = \
            self.session_stats['strategies_used'].get(strategy_type, 0) + 1
        
        # Update average confidence
        confidence = emotion_result.get('confidence', 0.0) * 100
        current_avg = self.session_stats['average_confidence']
        message_count = self.session_stats['messages_processed']
        
        # Calculate running average
        self.session_stats['average_confidence'] = \
            ((current_avg * (message_count - 1)) + confidence) / message_count
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        if not self.conversation_history:
            return {'summary': 'No conversation history available'}
        
        recent_topics = []
        recent_emotions = []
        
        # Analyze last 10 messages
        for entry in self.conversation_history[-10:]:
            if entry['topic'] not in recent_topics:
                recent_topics.append(entry['topic'])
            if entry['emotion'] not in recent_emotions:
                recent_emotions.append(entry['emotion'])
        
        return {
            'message_count': len(self.conversation_history),
            'session_duration': str(datetime.now() - self.session_stats['session_start']).split('.')[0],
            'recent_topics': recent_topics,
            'recent_emotions': recent_emotions,
            'conversation_stage': self.conversation_history[-1]['conversation_stage'] if self.conversation_history else 'opening',
            'average_confidence': f"{self.session_stats['average_confidence']:.1f}%",
            'most_discussed_topic': max(self.session_stats['topics_discussed'].items(), key=lambda x: x[1])[0] if self.session_stats['topics_discussed'] else 'none',
            'most_common_emotion': max(self.session_stats['emotions_detected'].items(), key=lambda x: x[1])[0] if self.session_stats['emotions_detected'] else 'none'
        }
    
    def get_user_insights(self) -> Dict[str, Any]:
        """Get insights about user based on conversation history"""
        user_profile = self.context_engine.user_profile
        
        # Personality insights
        personality = user_profile['personality_indicators']
        dominant_trait = max(personality.items(), key=lambda x: x[1])
        
        # Communication style
        comm_prefs = user_profile['communication_preferences']
        
        # Learning patterns
        analytics = self.context_engine.get_analytics()
        
        return {
            'personality_profile': {
                'dominant_trait': f"{dominant_trait[0]} ({dominant_trait[1]:.1%})",
                'analytical_tendency': f"{personality['analytical']:.1%}",
                'emotional_tendency': f"{personality['emotional']:.1%}",
                'creative_tendency': f"{personality['creative']:.1%}"
            },
            'communication_style': {
                'preferred_detail_level': 'High' if comm_prefs['detail_level'] > 0.6 else 'Medium' if comm_prefs['detail_level'] > 0.3 else 'Low',
                'formality_preference': 'Formal' if comm_prefs['formality'] > 0.6 else 'Professional' if comm_prefs['formality'] > 0.3 else 'Casual',
                'directness_preference': 'Direct' if comm_prefs['directness'] > 0.6 else 'Balanced' if comm_prefs['directness'] > 0.3 else 'Indirect'
            },
            'interests_and_patterns': {
                'top_topics': list(analytics['conversation_patterns']['topic_distribution'].keys())[:3],
                'profile_maturity': f"{analytics['user_profile_maturity']['personality_confidence']:.1%}",
                'learning_style': user_profile['learning_style']
            }
        }
    
    def reset_session(self):
        """Reset session statistics while preserving user profile"""
        self.session_stats = {
            'messages_processed': 0,
            'total_processing_time': 0,
            'average_confidence': 0,
            'emotions_detected': {},
            'topics_discussed': {},
            'strategies_used': {},
            'session_start': datetime.now()
        }
        self.conversation_history = []
        self.logger.info("Session reset - user profile preserved")

# Example usage and testing
if __name__ == "__main__":
    print("🤖 Enhanced Rudh Core - Phase 2.2")
    print("Advanced emotion detection + context-aware responses")
    print("="*60)
    
    async def test_enhanced_core():
        # Initialize enhanced core
        rudh = EnhancedRudhCore()
        
        # Test scenarios
        test_scenarios = [
            "I'm feeling really stressed about this work deadline coming up",
            "Can you help me understand how to invest in the stock market?",
            "My friend and I had a big argument, and I'm feeling sad about it",
            "Thank you for all the help! This conversation has been really valuable",
            "I'm excited about starting this new creative project but need some guidance"
        ]
        
        print("\n🧪 Testing Enhanced Rudh Core:")
        
        for i, message in enumerate(test_scenarios, 1):
            print(f"\n--- Test {i} ---")
            print(f"User: {message}")
            
            # Process message
            start_time = time.time()
            result = await rudh.process_message(message)
            processing_time = time.time() - start_time
            
            # Display results
            print(f"Rudh: {result['response']}")
            print(f"\n📊 Analysis:")
            print(f"   Emotion: {result['emotion_analysis']['primary_emotion']} ({result['emotion_analysis']['confidence']:.1%} confidence)")
            print(f"   Topic: {result['context_analysis']['topic']}")
            print(f"   Strategy: {result['response_strategy']['strategy_type']} ({result['response_strategy']['confidence']:.1%} confidence)")
            print(f"   Goals: {', '.join(result['context_analysis']['user_goals'])}")
            print(f"   Processing Time: {result['performance_metrics']['total_processing_time']}")
            
            # Small delay for demonstration
            await asyncio.sleep(0.5)
        
        # Display session summary
        print(f"\n📈 Session Summary:")
        summary = rudh.get_conversation_summary()
        for key, value in summary.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Display user insights
        print(f"\n👤 User Insights:")
        insights = rudh.get_user_insights()
        print(f"   Dominant Personality Trait: {insights['personality_profile']['dominant_trait']}")
        print(f"   Communication Style: {insights['communication_style']['preferred_detail_level']} detail, {insights['communication_style']['formality_preference']} tone")
        print(f"   Top Interests: {', '.join(insights['interests_and_patterns']['top_topics'])}")
        
        print(f"\n🎉 Enhanced Rudh Core test complete!")
        print("Context-aware AI with emotion intelligence ready for deployment!")
    
    # Run the test
    asyncio.run(test_enhanced_core())