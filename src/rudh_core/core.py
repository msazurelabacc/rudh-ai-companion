"""
Rudh Core - The main brain of your AI companion
"""
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from azure.identity import DefaultAzureCredential
import openai
import os

class RudhCore:
    """
    Main Rudh AI Core - The brain of your AI companion
    Handles conversation, emotion, and intelligence coordination
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.conversation_memory = []
        self.user_context = {}
        self.emotional_state = "neutral"
        self.personality_mode = "empathetic_companion"
        self.logger = self._setup_logging()
        self.openai_client = None
        self.is_initialized = False
        
    def _setup_logging(self):
        """Setup comprehensive logging for Rudh"""
        # Create logs directory if it doesn't exist
        log_dir = "C:\\RudhDev\\Logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}\\rudh_core.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('RudhCore')
    
    async def initialize(self):
        """Initialize Rudh with Azure services"""
        self.logger.info("🧠 Initializing Rudh AI Core...")
        
        try:
            # Initialize Azure OpenAI
            await self._initialize_openai()
            
            # Initialize other cognitive services
            await self._initialize_cognitive_services()
            
            # Load personality configuration
            self._load_personality()
            
            self.is_initialized = True
            self.logger.info("✅ Rudh Core initialized successfully!")
            
            # Send initial greeting
            await self._send_startup_message()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Rudh: {e}")
            return False
    
    async def _initialize_openai(self):
        """Initialize Azure OpenAI connection"""
        try:
            # For now, use environment variables
            # Later we'll move to Azure Key Vault
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            
            if not api_key or not endpoint:
                self.logger.warning("⚠️ Azure OpenAI credentials not found. Using mock responses.")
                self.openai_client = None
                return
            
            self.openai_client = openai.AzureOpenAI(
                api_key=api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=endpoint
            )
            
            self.logger.info("✅ Azure OpenAI initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize OpenAI: {e}")
            self.openai_client = None
    
    async def _initialize_cognitive_services(self):
        """Initialize other Azure AI services"""
        self.logger.info("🔧 Initializing cognitive services...")
        # Placeholder for Speech, Translator, etc.
        # We'll implement these in the next phase
        pass
    
    def _load_personality(self):
        """Load Rudh's personality configuration"""
        self.personality = {
            "name": "Rudh",
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
        self.logger.info(f"🎭 Personality loaded: {self.personality['style']}")
    
    async def _send_startup_message(self):
        """Send Rudh's startup greeting"""
        greeting = """
🌟 வணக்கம்! Hello! I'm Rudh, your AI companion.

I'm here to help you with:
💡 Intelligent conversations and advice
💰 Financial insights and market analysis  
🎨 Creative projects and problem-solving
🌍 Multilingual communication (Tamil & English)
❤️ Emotional support and understanding

How can I assist you today?
        """
        self.logger.info(greeting)
    
    async def process_message(self, user_input: str, user_id: str = "default") -> Dict:
        """
        Main message processing - This is where Rudh thinks and responds
        """
        if not self.is_initialized:
            await self.initialize()
        
        try:
            self.logger.info(f"📥 Processing message from {user_id}: {user_input[:50]}...")
            
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
            
            self.logger.info(f"✅ Response generated for {user_id}")
            return response_package
            
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            return {
                "response": "I'm having trouble processing that right now. Let me try again. 🤔",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback": True
            }
    
    async def _analyze_emotion(self, text: str) -> Dict:
        """Analyze emotional content of user input"""
        # Simple emotion detection for now
        # We'll enhance this with Azure Cognitive Services later
        
        emotional_keywords = {
            "happy": ["happy", "great", "awesome", "excellent", "good", "wonderful"],
            "sad": ["sad", "terrible", "awful", "bad", "worried", "depressed"],
            "excited": ["excited", "amazing", "fantastic", "thrilled"],
            "angry": ["angry", "furious", "frustrated", "annoyed"],
            "confused": ["confused", "don't understand", "unclear", "help"],
            "grateful": ["thank", "thanks", "grateful", "appreciate"]
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
        
        # Financial queries
        if any(word in text_lower for word in ["stock", "investment", "money", "market", "finance"]):
            return "financial_advisor"
        
        # Creative requests
        elif any(word in text_lower for word in ["create", "design", "make", "build", "generate"]):
            return "creative_assistant"
        
        # Emotional support
        elif emotion_context["primary_emotion"] in ["sad", "worried", "angry", "confused"]:
            return "emotional_support"
        
        # Knowledge questions
        elif any(word in text_lower for word in ["what", "how", "why", "explain", "tell me"]):
            return "knowledge_sharing"
        
        # Default conversational
        else:
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
            return "வணக்கம்! நான் ருத், உங்கள் AI துணை. எப்படி உதவ முடியும்? 🙏"
        
        # Strategy-based responses
        responses = {
            "emotional_support": {
                "sad": "I understand you're feeling down. I'm here to listen and support you. 💙",
                "angry": "I can sense your frustration. Let's work through this together. 🤝",
                "confused": "It's okay to feel confused. Let me help clarify things for you. 🧭",
                "neutral": "I'm here to support you in whatever way you need. 💙"
            },
            "financial_advisor": "I'd be happy to help with financial insights! Could you tell me more about what you're looking for? 📊💰",
            "creative_assistant": "I love helping with creative projects! What would you like to create today? 🎨✨",
            "knowledge_sharing": "Great question! I enjoy sharing knowledge. Let me help you understand this better. 🧠📚",
            "conversational": {
                "happy": "I'm glad you're feeling positive! How can I help make your day even better? 😊",
                "neutral": "Hello! I'm Rudh, your AI companion. How can I assist you today? 🌟"
            }
        }
        
        if strategy in responses:
            if isinstance(responses[strategy], dict):
                return responses[strategy].get(emotion, responses[strategy].get("neutral", "How can I help you today? 🙏"))
            else:
                return responses[strategy]
        
        return "I'm here to help! Could you tell me more about what you need? 🤔"
    
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
        
        self.logger.info(f"💾 Conversation stored. Memory size: {len(self.conversation_memory)}")
    
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
            "uptime": "Active since startup"  # We'll improve this later
        }
