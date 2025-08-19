# src/rudh_core/response_generator.py
"""
Rudh AI Advanced Response Generator - Phase 2.3
Sophisticated response generation with personality adaptation and Azure AI integration
"""

import asyncio
import logging
import json
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

# Azure AI imports (with fallbacks)
try:
    from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
    from azure.ai.translation.text import TextTranslationClient
    from azure.core.credentials import AzureKeyCredential
    AZURE_SERVICES_AVAILABLE = True
except ImportError:
    AZURE_SERVICES_AVAILABLE = False
    print("Azure services not available - running in enhanced fallback mode")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class ResponseStyle(Enum):
    """Response style variations for personality adaptation"""
    EMPATHETIC = "empathetic"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    MOTIVATIONAL = "motivational"

class ContentType(Enum):
    """Types of content Rudh can generate"""
    CONVERSATION = "conversation"
    FINANCIAL_ADVICE = "financial_advice"
    CREATIVE_CONTENT = "creative_content"
    EDUCATIONAL = "educational"
    TECHNICAL = "technical"
    EMOTIONAL_SUPPORT = "emotional_support"

@dataclass
class ResponseContext:
    """Context for response generation"""
    user_emotion: str
    conversation_history: List[Dict]
    user_preferences: Dict
    topic_context: str
    urgency_level: str
    formality_level: str
    cultural_context: str = "tamil_english"
    session_data: Dict = None

@dataclass
class GeneratedResponse:
    """Generated response with metadata"""
    primary_response: str
    alternative_responses: List[str]
    response_style: ResponseStyle
    confidence_score: float
    reasoning: str
    suggestions: List[str]
    follow_up_questions: List[str]
    estimated_sentiment: str
    generation_time: float
    metadata: Dict

class AdvancedResponseGenerator:
    """
    Rudh's Advanced Response Generation Engine - Phase 2.3
    Combines emotional intelligence with Azure AI for sophisticated responses
    """
    
    def __init__(self, azure_config: Optional[Dict] = None):
        self.azure_config = azure_config or {}
        self.logger = logging.getLogger('ResponseGenerator')
        self.openai_client = None
        self.speech_synthesizer = None
        self.translator_client = None
        
        # Response templates organized by context and personality
        self.response_templates = self._initialize_response_templates()
        self.personality_traits = self._initialize_personality_traits()
        
        # Performance tracking
        self.generation_stats = {
            'total_responses': 0,
            'avg_generation_time': 0.0,
            'style_distribution': {},
            'success_rate': 0.0
        }
        
    async def initialize_azure_services(self):
        """Initialize Azure AI services for production-grade responses"""
        try:
            if not AZURE_SERVICES_AVAILABLE:
                self.logger.warning("Azure services not available. Using enhanced fallback mode.")
                return False
                
            # Initialize Azure OpenAI
            await self._initialize_azure_openai()
            
            # Initialize Speech Services
            await self._initialize_speech_services()
            
            # Initialize Translator
            await self._initialize_translator()
            
            self.logger.info("Azure AI services initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure services: {e}")
            return False
    
    async def generate_response(self, user_input: str, context: ResponseContext) -> GeneratedResponse:
        """
        Generate sophisticated response using context and Azure AI
        """
        start_time = datetime.now()
        
        try:
            # Analyze response requirements
            response_requirements = await self._analyze_response_requirements(user_input, context)
            
            # Select optimal response style
            response_style = self._select_response_style(context, response_requirements)
            
            # Generate primary response
            primary_response = await self._generate_primary_response(
                user_input, context, response_style, response_requirements
            )
            
            # Generate alternatives
            alternatives = await self._generate_alternative_responses(
                user_input, context, response_style, 2
            )
            
            # Generate follow-up suggestions
            suggestions, follow_ups = await self._generate_follow_ups(
                user_input, context, primary_response
            )
            
            # Calculate confidence and reasoning
            confidence, reasoning = self._calculate_response_confidence(
                primary_response, context, response_requirements
            )
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Update statistics
            self._update_generation_stats(response_style, generation_time, confidence)
            
            return GeneratedResponse(
                primary_response=primary_response,
                alternative_responses=alternatives,
                response_style=response_style,
                confidence_score=confidence,
                reasoning=reasoning,
                suggestions=suggestions,
                follow_up_questions=follow_ups,
                estimated_sentiment=self._estimate_response_sentiment(primary_response),
                generation_time=generation_time,
                metadata={
                    'requirements': response_requirements,
                    'azure_enhanced': self.openai_client is not None,
                    'template_used': response_requirements.get('template_category'),
                    'cultural_adaptation': context.cultural_context
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return await self._generate_fallback_response(user_input, context)
    
    async def _generate_primary_response(self, user_input: str, context: ResponseContext, 
                                       style: ResponseStyle, requirements: Dict) -> str:
        """Generate the main response using Azure OpenAI or advanced fallback"""
        
        if self.openai_client and OPENAI_AVAILABLE:
            return await self._generate_azure_openai_response(user_input, context, style, requirements)
        else:
            return await self._generate_enhanced_fallback_response(user_input, context, style, requirements)
    
    async def _generate_azure_openai_response(self, user_input: str, context: ResponseContext,
                                            style: ResponseStyle, requirements: Dict) -> str:
        """Generate response using Azure OpenAI GPT-4"""
        try:
            # Build sophisticated system prompt
            system_prompt = self._build_azure_system_prompt(context, style, requirements)
            
            # Prepare conversation history
            messages = self._prepare_conversation_history(context, system_prompt, user_input)
            
            # Generate response with Azure OpenAI
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",  # or your deployed model name
                messages=messages,
                max_tokens=800,
                temperature=self._get_temperature_for_style(style),
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            generated_text = response.choices[0].message.content
            
            # Apply Rudh's personality filters
            return self._apply_personality_adaptation(generated_text, context, style)
            
        except Exception as e:
            self.logger.error(f"Azure OpenAI generation failed: {e}")
            # Fallback to enhanced local generation
            return await self._generate_enhanced_fallback_response(user_input, context, style, requirements)
    
    async def _generate_enhanced_fallback_response(self, user_input: str, context: ResponseContext,
                                                 style: ResponseStyle, requirements: Dict) -> str:
        """Enhanced fallback response generation with sophisticated templates"""
        
        # Select appropriate template category
        template_category = requirements.get('template_category', 'general')
        
        # Get templates for this category and style
        templates = self.response_templates.get(template_category, {}).get(style.value, [])
        
        if not templates:
            # Fallback to general templates
            templates = self.response_templates.get('general', {}).get(style.value, [])
        
        # Select best template based on context
        selected_template = self._select_best_template(templates, context, requirements)
        
        # Fill template with context-specific content
        response = self._fill_response_template(selected_template, user_input, context, requirements)
        
        # Apply personality and cultural adaptations
        response = self._apply_personality_adaptation(response, context, style)
        
        return response
    
    def _build_azure_system_prompt(self, context: ResponseContext, style: ResponseStyle, 
                                 requirements: Dict) -> str:
        """Build sophisticated system prompt for Azure OpenAI"""
        
        personality_description = self.personality_traits[style.value]
        
        system_prompt = f"""You are Rudh, an advanced AI companion with deep emotional intelligence and cultural awareness.

PERSONALITY & STYLE:
{personality_description}

CURRENT CONTEXT:
- User Emotion: {context.user_emotion}
- Topic: {context.topic_context}
- Urgency: {context.urgency_level}
- Formality: {context.formality_level}
- Cultural Context: {context.cultural_context}

RESPONSE REQUIREMENTS:
- Style: {style.value}
- Content Type: {requirements.get('content_type', 'conversation')}
- Key Elements: {', '.join(requirements.get('key_elements', []))}

GUIDELINES:
1. Be empathetic and emotionally intelligent
2. Adapt your communication style to match the context
3. Provide actionable insights when appropriate
4. Use Tamil phrases naturally when culturally relevant
5. Be concise but comprehensive
6. Show genuine understanding and care

Respond as Rudh would, keeping these elements in perfect balance."""

        return system_prompt
    
    def _initialize_response_templates(self) -> Dict:
        """Initialize sophisticated response templates"""
        return {
            'emotional_support': {
                'empathetic': [
                    "I can really understand how {emotion} you must be feeling about {context}. {validation_statement} {support_offer}",
                    "That sounds incredibly {emotion_intensity}. I hear that you're feeling {emotion}, and that's completely understandable given {context}. {empathy_bridge} {next_step}",
                    "Your feelings about {context} are completely valid. It takes courage to share when you're feeling {emotion}. {understanding_reflection} {supportive_guidance}"
                ],
                'analytical': [
                    "Looking at your situation with {context}, I can identify several factors contributing to your {emotion} feelings. {analysis_intro} {structured_breakdown} {actionable_next_steps}",
                    "Let me help you break down what's happening with {context}. The {emotion} you're experiencing likely stems from {causal_analysis}. {solution_framework}"
                ],
                'motivational': [
                    "I hear that you're facing challenges with {context} and feeling {emotion}. This is exactly the kind of situation where your inner strength can emerge. {empowerment_message} {action_motivation}",
                    "Feeling {emotion} about {context} shows that you care deeply, which is actually a strength. {strength_recognition} {motivational_reframe} {forward_action}"
                ]
            },
            'financial_advice': {
                'analytical': [
                    "Based on your financial query about {topic}, here's my analysis: {financial_assessment} {risk_analysis} {recommendation_framework} {next_steps}",
                    "Looking at the {financial_context} market conditions, I can provide these insights: {market_analysis} {strategic_recommendation} {implementation_guidance}"
                ],
                'professional': [
                    "Regarding your investment question about {topic}: {professional_assessment} {evidence_based_analysis} {structured_recommendation} {risk_disclosure}",
                    "For your financial planning needs around {topic}: {comprehensive_analysis} {tailored_strategy} {execution_plan} {monitoring_framework}"
                ]
            },
            'creative_content': {
                'creative': [
                    "What an exciting creative challenge! For {creative_topic}, I envision: {creative_vision} {innovative_elements} {implementation_approach} {enhancement_ideas}",
                    "I love the creative potential in {creative_topic}! Here's my inspired approach: {artistic_concept} {unique_features} {development_strategy} {creative_evolution}"
                ],
                'analytical': [
                    "For your creative project involving {creative_topic}, let me structure this systematically: {project_analysis} {resource_requirements} {development_phases} {success_metrics}"
                ]
            },
            'general': {
                'empathetic': [
                    "I appreciate you sharing this with me. {acknowledgment} {empathetic_response} {gentle_guidance}",
                    "Thank you for trusting me with your thoughts about {topic}. {understanding_statement} {supportive_insight} {collaborative_next_step}"
                ],
                'conversational': [
                    "That's really interesting! {engagement_statement} {thoughtful_response} {curious_follow_up}",
                    "I can see why {topic} would be on your mind. {relatable_insight} {balanced_perspective} {engaging_question}"
                ],
                'professional': [
                    "Regarding {topic}: {professional_acknowledgment} {expert_insight} {structured_guidance} {clear_next_steps}",
                    "I understand your question about {topic}. {competent_assessment} {evidence_based_response} {actionable_recommendations}"
                ]
            }
        }
    
    def _initialize_personality_traits(self) -> Dict:
        """Initialize Rudh's personality traits for each response style"""
        return {
            'empathetic': """
You embody warmth, understanding, and emotional intelligence. You listen deeply, 
validate feelings, and provide gentle guidance. Your responses show genuine care 
and create a safe space for vulnerable sharing. You're intuitive about emotional 
needs and respond with compassion while maintaining helpful boundaries.
            """.strip(),
            
            'analytical': """
You approach situations with systematic thinking and logical frameworks. You break 
down complex problems, identify patterns, and provide structured solutions. Your 
responses are data-informed, methodical, and thorough while remaining accessible 
and practical. You help users think through problems step-by-step.
            """.strip(),
            
            'creative': """
You bring imagination, innovation, and artistic vision to every interaction. You 
see possibilities others might miss, suggest unique approaches, and inspire 
original thinking. Your responses are dynamic, visually engaging, and full of 
creative energy while remaining grounded in practical implementation.
            """.strip(),
            
            'professional': """
You maintain expertise, competence, and reliability in all interactions. You 
provide authoritative guidance based on best practices and industry standards. 
Your responses are polished, well-structured, and demonstrate deep knowledge 
while being clear and actionable.
            """.strip(),
            
            'casual': """
You communicate in a friendly, relaxed, and approachable manner. You use natural 
language, appropriate humor, and create a comfortable conversational atmosphere. 
Your responses feel like talking with a knowledgeable friend who genuinely cares 
about helping you succeed.
            """.strip(),
            
            'motivational': """
You inspire action, build confidence, and empower positive change. You focus on 
strengths, possibilities, and growth opportunities. Your responses energize and 
encourage while providing practical steps toward goals. You help users see their 
potential and take meaningful action.
            """.strip()
        }
    
    # Additional helper methods would continue here...
    # (truncated for length, but would include all template filling, 
    # personality adaptation, Azure service initialization, etc.)

    def get_generation_stats(self) -> Dict:
        """Get current generation statistics"""
        return {
            **self.generation_stats,
            'azure_services_active': self.openai_client is not None,
            'available_styles': list(ResponseStyle),
            'template_categories': list(self.response_templates.keys())
        }