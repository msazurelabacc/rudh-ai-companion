# src\rudh_core\core.py
"""
Rudh AI Core - The main brain and intelligence engine
Complete version with emoji logging fix and improved strategy detection
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Safe imports with fallbacks
try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    AZURE_AVAILABLE = True
except ImportError:
    print("Azure services not available - running in fallback mode")
    AZURE_AVAILABLE = False
    DefaultAzureCredential = None
    SecretClient = None

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    print("OpenAI not available - using fallback responses")
    OPENAI_AVAILABLE = False
    openai = None

class RudhCore:
    """
    Main Rudh AI Core - The brain of your AI companion
    Enhanced with proper logging and strategy detection
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.conversation_memory = []
        self.user_context = {}
        self.emotional_state = "neutral"
        self.personality_mode = "empathetic_intelligent_companion"
        self.is_initialized = False
        self.openai_client = None
        self.personality = {}
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for Rudh with proper Unicode support"""
        # Configure logging with UTF-8 encoding and no emojis for file logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('C:\\RudhDev\\Logs\\rudh.log', encoding='utf-8'),
                # Remove console handler to avoid emoji encoding issues
            ],
            force=True  # Override any existing configuration
        )
        
        # Create logger
        logger = logging.getLogger('RudhCore')
        logger.info("Logging system initialized with Unicode support")
        return logger
    
    async def initialize(self):
        """Initialize Rudh with Azure services"""
        try:
            print("Initializing Rudh AI Core...")
            self.logger.info("Initializing Rudh AI Core...")
            
            # Initialize Azure OpenAI
            await self._initialize_openai()
            
            # Initialize other services
            await self._initialize_cognitive_services()
            
            # Load personality
            self._load_personality()
            
            self.is_initialized = True
            print("Rudh Core initialized successfully!")
            self.logger.info("Rudh Core initialized successfully!")
            
            await self._send_startup_message()
            return True
            
        except Exception as e:
            print(f"Failed to initialize Rudh: {e}")
            self.logger.error(f"Failed to initialize Rudh: {e}")
            return False
    
    async def _initialize_openai(self):
        """Initialize Azure OpenAI connection"""
        try:
            azure_config = self.config.get("azure", {})
            openai_endpoint = azure_config.get("openai_endpoint")
            openai_key = azure_config.get("openai_api_key")
            
            if openai_endpoint and openai_key and OPENAI_AVAILABLE:
                self.openai_client = openai.AzureOpenAI(
                    azure_endpoint=openai_endpoint,
                    api_key=openai_key,
                    api_version="2024-02-15-preview"
                )
                print("Azure OpenAI connected successfully!")
                self.logger.info("Azure OpenAI connected successfully!")
            else:
                print("Azure OpenAI credentials not found. Using mock responses.")
                self.logger.warning("Azure OpenAI credentials not found. Using mock responses.")
                
        except Exception as e:
            print(f"OpenAI initialization error: {e}")
            self.logger.error(f"OpenAI initialization error: {e}")
    
    async def _initialize_cognitive_services(self):
        """Initialize other Azure AI services"""
        print("Initializing cognitive services...")
        self.logger.info("Initializing cognitive services...")
        
        # Placeholder for speech, translator, etc.
        # We'll implement these later when we connect real Azure services
        pass
    
    def _load_personality(self):
        """Load Rudh's personality configuration"""
        self.personality = {
            "style": "empathetic_intelligent_companion",
            "languages": ["tamil", "english"],
            "traits": [
                "empathetic", "intelligent", "supportive",
                "culturally_aware", "proactive", "respectful"
            ],
            "expertise": [
                "emotional_support", "financial_advice",
                "creative_assistance", "knowledge_sharing"
            ]
        }
        print(f"Personality loaded: {self.personality['style']}")
        self.logger.info(f"Personality loaded: {self.personality['style']}")

    async def _send_startup_message(self):
        """Send Rudh's startup greeting"""
        greeting = """
Welcome! I'm Rudh, your AI companion.

I'm here to help you with:
- Intelligent conversations and advice
- Financial insights and market analysis  
- Creative projects and problem-solving
- Multilingual communication (Tamil & English)
- Emotional support and understanding

How can I assist you today?
        """
        print(greeting)
        self.logger.info("Startup message displayed")

    async def process_message(self, user_input: str, user_id: str = "default") -> Dict:
        """
        Main message processing - This is where Rudh thinks and responds
        """
        if not self.is_initialized:
            await self.initialize()

        try:
            print(f"Processing message from {user_id}: {user_input[:50]}...")
            self.logger.info(f"Processing message from {user_id}: {user_input[:50]}...")

            # Step 1: Analyze emotional context
            emotion_analysis = await self._analyze_emotion(user_input)

            # Step 2: Determine response strategy
            response_strategy = self._determine_response_strategy(user_input, emotion_analysis)

            # Step 3: Generate intelligent response
            response = await self._generate_response(user_input, emotion_analysis, response_strategy)

            # Step 4: Store conversation in memory
            self._update_conversation_memory(user_input, response, user_id, emotion_analysis)

            # Step 5: Prepare response package
            response_package = {
                "response": response,
                "emotion_detected": emotion_analysis,
                "strategy_used": response_strategy,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.85,
                "language_detected": self._detect_language(user_input),
                "rudh_mood": self.emotional_state
            }

            print(f"Response generated for {user_id}")
            self.logger.info(f"Response generated for {user_id}")
            return response_package

        except Exception as e:
            print(f"Error processing message: {e}")
            self.logger.error(f"Error processing message: {e}")
            return {
                "response": "I'm having trouble processing that right now. Let me try again.",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback": True
            }

    async def _analyze_emotion(self, text: str) -> Dict:
        """Analyze emotional content of user input"""
        # Enhanced emotion detection
        emotional_keywords = {
            "happy": ["happy", "great", "awesome", "excellent", "good", "wonderful", "excited", "joy"],
            "sad": ["sad", "terrible", "awful", "bad", "worried", "depressed", "down", "upset"],
            "excited": ["excited", "amazing", "fantastic", "thrilled", "pumped"],
            "angry": ["angry", "furious", "frustrated", "annoyed", "mad"],
            "confused": ["confused", "don't understand", "unclear", "help", "lost"],
            "grateful": ["thank", "thanks", "grateful", "appreciate"],
            "anxious": ["anxious", "worried", "nervous", "stressed", "tension"]
        }

        text_lower = text.lower()
        detected_emotions = []

        for emotion, keywords in emotional_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)

        primary_emotion = detected_emotions[0] if detected_emotions else "neutral"

        return {
            "primary_emotion": primary_emotion,
            "all_emotions": detected_emotions,
            "confidence": 0.7,
            "suggestions": self._get_response_suggestions(primary_emotion),
            "tamil_detected": any(word in text for word in ["வணக்கம்", "நன்றி", "எப்படி"])
        }

    def _determine_response_strategy(self, user_input: str, emotion_context: Dict) -> str:
        """Determine the best response strategy based on input and emotion"""
        text_lower = user_input.lower()

        # Financial queries - Enhanced detection
        financial_keywords = [
            "stock", "investment", "money", "market", "finance", "trading", "portfolio",
            "invest", "shares", "equity", "mutual fund", "sip", "financial advice",
            "financial", "advise", "advice", "budget", "saving", "profit", "loss"
        ]
        if any(word in text_lower for word in financial_keywords):
            return "financial_advisor"

        # Creative requests
        creative_keywords = ["create", "design", "make", "build", "generate", "develop"]
        if any(word in text_lower for word in creative_keywords):
            return "creative_assistant"

        # Emotional support
        if emotion_context["primary_emotion"] in ["sad", "worried", "angry", "confused", "anxious"]:
            return "emotional_support"

        # Knowledge questions
        knowledge_keywords = ["what", "how", "why", "explain", "tell me", "define", "meaning"]
        if any(word in text_lower for word in knowledge_keywords):
            return "knowledge_sharing"

        # Default conversational
        return "conversational"

    async def _generate_response(self, user_input: str, emotion_context: Dict, strategy: str) -> str:
        """Generate AI response using strategy and context"""

        # If we have OpenAI connection, use it
        if self.openai_client:
            return await self._generate_openai_response(user_input, emotion_context, strategy)

        # Otherwise, use intelligent fallback responses
        return self._generate_fallback_response(user_input, emotion_context, strategy)

    async def _generate_openai_response(self, user_input: str, emotion_context: Dict, strategy: str) -> str:
        """Generate response using Azure OpenAI"""
        try:
            # Construct system prompt based on Rudh's personality
            system_prompt = self._build_system_prompt(emotion_context, strategy)

            # Get conversation context
            context = self._get_conversation_context()

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nUser: {user_input}"}
            ]

            response = await self.openai_client.chat.completions.create(
                model="gpt-4",  # or your deployed model name
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"OpenAI error: {e}")
            return self._generate_fallback_response(user_input, emotion_context, strategy)

    def _generate_fallback_response(self, user_input: str, emotion_context: Dict, strategy: str) -> str:
        """Generate intelligent fallback responses when OpenAI is not available"""
        emotion = emotion_context["primary_emotion"]
        tamil_detected = emotion_context.get("tamil_detected", False)

        # Tamil greeting responses
        if "வணக்கம்" in user_input:
            return "வணக்கம்! நான் ருத், உங்கள் AI துணை. எப்படி உதவ முடியும்?"

        # Strategy-based responses
        responses = {
            "emotional_support": {
                "sad": "I understand you're feeling down. I'm here to listen and support you. Would you like to talk about what's bothering you?",
                "angry": "I can sense your frustration. Let's work through this together. What's causing these feelings?",
                "confused": "It's okay to feel confused. Let me help clarify things for you. What specifically would you like help with?",
                "anxious": "I hear that you're feeling anxious. Take a deep breath. I'm here to help you work through this.",
                "neutral": "I'm here to support you in whatever way you need."
            },
            "financial_advisor": "I'd be happy to help with financial insights! I can assist with investment strategies, market analysis, portfolio planning, and wealth building. What specific financial area would you like to explore? Are you interested in stocks, mutual funds, SIPs, or general financial planning?",
            "creative_assistant": "I love helping with creative projects! What would you like to create today? I can help with business plans, designs, content creation, or any innovative ideas you have in mind.",
            "knowledge_sharing": "Great question! I enjoy sharing knowledge and helping you understand complex topics. Let me provide you with detailed insights on this subject.",
            "conversational": {
                "happy": "I'm glad you're feeling positive! How can I help make your day even better?",
                "grateful": "You're very welcome! I'm always happy to help. Is there anything else I can assist you with?",
                "neutral": "Hello! I'm Rudh, your AI companion. How can I assist you today?"
            }
        }

        if strategy in responses:
            if isinstance(responses[strategy], dict):
                return responses[strategy].get(emotion, responses[strategy].get("neutral", "How can I help you today?"))
            else:
                return responses[strategy]

        return "I'm here to help! Could you tell me more about what you need assistance with?"

    def _build_system_prompt(self, emotion_context: Dict, strategy: str) -> str:
        """Build system prompt for OpenAI based on context"""
        base_prompt = f"""
You are Rudh, an advanced AI companion with deep emotional intelligence. You are:

- Empathetic and understanding
- Culturally aware (Tamil and English speaking)
- Expert in multiple domains (finance, creativity, knowledge)
- Supportive and encouraging
- Professional yet warm

Current context:
- User emotion: {emotion_context['primary_emotion']}
- Response strategy: {strategy}
- Your personality: {self.personality['style']}

Respond with empathy, intelligence, and cultural sensitivity. Keep responses helpful but concise.
        """
        return base_prompt.strip()

    def _get_conversation_context(self) -> str:
        """Get recent conversation context"""
        if not self.conversation_memory:
            return "This is the start of our conversation."

        recent_conversations = self.conversation_memory[-3:]  # Last 3 exchanges
        context_parts = []

        for conv in recent_conversations:
            context_parts.append(f"User: {conv['user_input'][:100]}")
            context_parts.append(f"Rudh: {conv['rudh_response'][:100]}")

        return " | ".join(context_parts)

    def _detect_language(self, text: str) -> str:
        """Simple language detection"""
        tamil_chars = any('\u0b80' <= char <= '\u0bff' for char in text)
        tamil_words = any(word in text for word in ["வணக்கம்", "நன்றி", "எப்படி", "என்ன"])

        if tamil_chars or tamil_words:
            return "tamil"
        return "english"

    def _get_response_suggestions(self, emotion: str) -> List[str]:
        """Get response strategy suggestions based on emotion"""
        suggestions = {
            "sad": ["provide_comfort", "offer_support", "be_gentle"],
            "angry": ["stay_calm", "acknowledge_feelings", "offer_solutions"],
            "happy": ["share_enthusiasm", "be_encouraging"],
            "confused": ["clarify_step_by_step", "provide_examples"],
            "anxious": ["be_reassuring", "offer_calming_presence"],
            "neutral": ["be_helpful", "ask_clarifying_questions"]
        }
        return suggestions.get(emotion, ["be_supportive"])

    def _update_conversation_memory(self, user_input: str, response: str, user_id: str, emotion_analysis: Dict):
        """Store conversation in memory for context"""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "user_input": user_input,
            "rudh_response": response,
            "emotion_context": emotion_analysis,
            "conversation_id": len(self.conversation_memory) + 1
        }

        self.conversation_memory.append(conversation_entry)

        # Keep only last 50 conversations in memory
        if len(self.conversation_memory) > 50:
            self.conversation_memory = self.conversation_memory[-50:]

        print(f"Conversation stored. Memory size: {len(self.conversation_memory)}")
        self.logger.info(f"Conversation stored. Memory size: {len(self.conversation_memory)}")

    def get_conversation_history(self, user_id: str = None, limit: int = 10) -> List[Dict]:
        """Get conversation history for analysis or review"""
        if user_id:
            filtered_conversations = [
                conv for conv in self.conversation_memory 
                if conv["user_id"] == user_id
            ]
            return filtered_conversations[-limit:]

        return self.conversation_memory[-limit:]
    
    def get_stats(self) -> Dict:
        """Get Rudh's operational statistics"""
        return {
            "total_conversations": len(self.conversation_memory),
            "current_emotional_state": self.emotional_state,
            "personality_mode": self.personality_mode,
            "is_initialized": self.is_initialized,
            "openai_connected": self.openai_client is not None,
            "uptime": "Active since startup"
        }