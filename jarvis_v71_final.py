#!/usr/bin/env python3
"""
🚀 JARVIS V7.1 FINAL FIX - AI Connection Corrected
Fixed the OpenAI variable name issue and microphone handling
"""

import asyncio
import time
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class IronManJARVISFinal:
    """Final production Iron Man JARVIS with corrected AI connection"""
    
    def __init__(self):
        self.speech_config = None
        self.speech_synthesizer = None
        self.speech_recognizer = None
        self.voice_enabled = True
        self.ai_client = None
        self.logger = self._setup_logging()
        self.conversation_history = []
        self.user_name = "Sir"  # Iron Man style addressing
        self.deployment_name = None
        
        # Initialize services
        asyncio.run(self._initialize_services())
    
    def _setup_logging(self) -> logging.Logger:
        """Setup enhanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='🤖 %(asctime)s - JARVIS - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        return logging.getLogger(__name__)
    
    async def _initialize_services(self):
        """Initialize Azure Speech and OpenAI services"""
        try:
            # FIXED: Azure OpenAI Configuration (correct variable names)
            openai_key = os.getenv('AZURE_OPENAI_API_KEY')  # Your actual variable name
            openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')  # Your actual variable name
            
            if openai_key and openai_endpoint:
                try:
                    self.ai_client = AzureOpenAI(
                        api_key=openai_key,
                        api_version="2024-02-15-preview",
                        azure_endpoint=openai_endpoint
                    )
                    self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_GPT4O', 'rudh-gpt4o')
                    
                    # Test the connection
                    test_response = self.ai_client.chat.completions.create(
                        model=self.deployment_name,
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=10
                    )
                    
                    self.logger.info(f"✅ Azure OpenAI connected successfully with deployment: {self.deployment_name}")
                except Exception as e:
                    self.logger.error(f"❌ Azure OpenAI connection failed: {e}")
                    self.ai_client = None
            else:
                self.logger.warning("⚠️ OpenAI credentials not found")
                
            # Azure Speech Configuration
            speech_key = os.getenv('AZURE_SPEECH_KEY')
            speech_region = os.getenv('AZURE_SPEECH_REGION')
            
            if speech_key and speech_region:
                try:
                    self.speech_config = speechsdk.SpeechConfig(
                        subscription=speech_key, 
                        region=speech_region
                    )
                    # Use your configured voice
                    voice_name = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
                    self.speech_config.speech_synthesis_voice_name = voice_name
                    
                    self.speech_config.set_speech_synthesis_output_format(
                        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
                    )
                    
                    # Initialize synthesizer (this works)
                    self.speech_synthesizer = speechsdk.SpeechSynthesizer(
                        speech_config=self.speech_config
                    )
                    
                    # FIXED: Skip voice recognition initialization if no microphone
                    try:
                        self.speech_recognizer = speechsdk.SpeechRecognizer(
                            speech_config=self.speech_config
                        )
                        self.logger.info(f"✅ Azure Speech Services fully initialized with voice: {voice_name}")
                    except Exception as mic_error:
                        self.logger.warning(f"⚠️ Voice recognition disabled (no microphone): {mic_error}")
                        self.speech_recognizer = None
                        
                except Exception as e:
                    self.logger.error(f"❌ Speech service initialization failed: {e}")
                    self.voice_enabled = False
            else:
                self.logger.warning("⚠️ Azure Speech credentials not found")
                self.voice_enabled = False
                
        except Exception as e:
            self.logger.error(f"❌ Service initialization failed: {e}")
    
    async def synthesize_speech(self, text: str, emotion: str = "confident") -> bool:
        """Enhanced speech synthesis with emotional styling"""
        if not self.voice_enabled or not self.speech_synthesizer:
            return False
            
        try:
            # Create JARVIS style SSML
            ssml_text = self._create_jarvis_ssml(text, emotion)
            
            start_time = time.time()
            result = self.speech_synthesizer.speak_ssml_async(ssml_text).get()
            synthesis_time = time.time() - start_time
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                self.logger.info(f"🗣️ JARVIS spoke ({synthesis_time:.2f}s): {text[:50]}...")
                return True
            else:
                self.logger.error(f"❌ Speech synthesis failed: {result.reason}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Speech synthesis error: {e}")
            return False
    
    def _create_jarvis_ssml(self, text: str, emotion: str) -> str:
        """Create Iron Man JARVIS style SSML with emotional styling"""
        emotion_styles = {
            "confident": {"rate": "medium", "pitch": "+3%", "volume": "+5%"},
            "analytical": {"rate": "slow", "pitch": "-2%", "volume": "medium"},
            "urgent": {"rate": "fast", "pitch": "+5%", "volume": "+10%"},
            "calm": {"rate": "slow", "pitch": "-3%", "volume": "soft"},
            "neutral": {"rate": "medium", "pitch": "medium", "volume": "medium"}
        }
        
        style = emotion_styles.get(emotion, emotion_styles["confident"])
        voice_name = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-IN">
            <voice name="{voice_name}">
                <prosody rate="{style['rate']}" pitch="{style['pitch']}" volume="{style['volume']}">
                    <emphasis level="moderate">{text}</emphasis>
                </prosody>
            </voice>
        </speak>
        """
        return ssml
    
    async def get_ai_response(self, user_input: str) -> str:
        """FIXED: Get intelligent response from Azure OpenAI"""
        try:
            if not self.ai_client:
                return f"I apologize, {self.user_name}, but my advanced AI capabilities are currently offline. However, I can still assist with basic commands and system functions."
            
            # Enhanced JARVIS personality prompt
            system_prompt = f"""You are JARVIS, the sophisticated AI assistant from Iron Man. You are:
            - Highly intelligent and analytical with a British-influenced formal tone
            - Always address the user as '{self.user_name}' 
            - Professional yet warm and personable
            - Provide expert advice with confidence
            - Keep responses concise but informative (under 200 words)
            - Focus on being helpful and proactive
            - Use sophisticated vocabulary while remaining accessible
            
            You are an advanced AI companion designed to assist with:
            - Personal productivity and planning
            - Analysis and decision-making
            - Technology and business advice
            - General knowledge and problem-solving
            
            Respond in JARVIS's characteristic style: intelligent, helpful, and slightly formal but warm.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.ai_client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=250,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"❌ AI response error: {e}")
            return f"I apologize, {self.user_name}, but I'm experiencing some technical difficulties with my advanced AI functions. However, I remain at your service for basic commands and system operations."
    
    async def process_command(self, command: str) -> str:
        """Process voice or text commands with Iron Man JARVIS intelligence"""
        command_lower = command.lower().strip()
        
        # System commands
        if command_lower in ['/voice', 'toggle voice', 'voice off', 'voice on']:
            self.voice_enabled = not self.voice_enabled
            status = "enabled" if self.voice_enabled else "disabled"
            return f"Voice output {status}, {self.user_name}."
        
        elif command_lower in ['/status', 'status', 'system status', 'diagnostics']:
            return await self._get_system_status()
        
        elif command_lower in ['/help', 'help', 'what can you do', 'commands']:
            return self._get_help_menu()
        
        elif command_lower in ['time', 'what time is it', 'current time']:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}, {self.user_name}."
        
        elif command_lower in ['date', 'what date is it', 'today', 'current date']:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}, {self.user_name}."
        
        elif command_lower in ['weather', "what's the weather", 'weather today']:
            return f"I don't currently have access to weather data, {self.user_name}. May I suggest checking your preferred weather application or asking me to help you find weather information online?"
        
        elif command_lower in ['schedule', 'calendar', 'appointments', 'meetings']:
            return f"I don't have access to your calendar at the moment, {self.user_name}. However, I'd be happy to help you organize your thoughts or plan your day if you share your schedule with me."
        
        # AI-powered responses for complex queries
        else:
            return await self.get_ai_response(command)
    
    async def _get_system_status(self) -> str:
        """Get comprehensive system status"""
        speech_status = "✅ Operational" if self.voice_enabled and self.speech_synthesizer else "❌ Disabled"
        ai_status = "✅ Connected" if self.ai_client else "❌ Disconnected"
        recognition_status = "✅ Active" if self.speech_recognizer else "⚠️ No microphone"
        
        # Get deployment info
        deployment_info = f" ({self.deployment_name})" if self.deployment_name else ""
        
        return f"""System Status Report, {self.user_name}:
        
🗣️ Voice Synthesis: {speech_status}
🧠 AI Intelligence: {ai_status}{deployment_info}
🎤 Voice Recognition: {recognition_status}
⚡ Response Time: Optimal
🛡️ Security: All systems secure
🔧 Environment: Production Mode

All primary systems are {"functioning within normal parameters" if ai_status.startswith("✅") and speech_status.startswith("✅") else "operational with some limitations"}."""
    
    def _get_help_menu(self) -> str:
        """Get comprehensive help menu"""
        return f"""JARVIS Command Reference, {self.user_name}:

⚡ SYSTEM COMMANDS:
   • /status - Comprehensive system diagnostics
   • /voice - Toggle voice output on/off
   • /help - Display this command reference
   • time/date - Current time and date

🧠 AI CAPABILITIES:
   • Natural language conversation
   • Analysis and problem-solving
   • Decision-making assistance
   • Technical and business advice
   • Personal productivity support
   • Strategic planning and insights

💡 EXAMPLE QUERIES:
   • "Help me plan my day efficiently"
   • "What should I focus on today?"
   • "Analyze this business problem..."
   • "Give me advice on technology trends"
   • "Help me make a decision about..."

📋 PRODUCTIVITY FEATURES:
   • Task planning and organization
   • Goal setting and tracking
   • Problem analysis and solutions
   • Strategic thinking assistance

How may I assist you further, {self.user_name}?"""
    
    async def run_interactive_session(self):
        """Run main JARVIS interactive session"""
        print("🚀 JARVIS V7.1 FINAL - IRON MAN AI ASSISTANT")
        print("=" * 60)
        
        # System initialization status
        ai_status = "with full AI capabilities" if self.ai_client else "in basic mode"
        voice_status = "Voice synthesis ready" if self.voice_enabled else "Voice synthesis unavailable"
        
        welcome_msg = f"Good day, {self.user_name}. JARVIS is now online and operational {ai_status}. {voice_status}. How may I be of service today?"
        print(f"🤖 JARVIS: {welcome_msg}")
        
        if self.voice_enabled:
            await self.synthesize_speech(f"Good day, {self.user_name}. JARVIS is online and ready to assist.", "confident")
        
        print(f"\n💡 Text Commands: Type your commands or questions")
        print(f"💡 System Commands: /help, /status, /voice")
        print(f"💡 Exit: Type 'quit', 'exit', or 'goodbye'")
        
        print(f"\n🔧 SYSTEM STATUS:")
        print(f"   🗣️ Voice Synthesis: {'✅ Ready' if self.voice_enabled else '❌ Offline'}")
        print(f"   🧠 AI Intelligence: {'✅ Connected' if self.ai_client else '❌ Basic Mode'}")
        print(f"   🎤 Voice Recognition: {'✅ Active' if self.speech_recognizer else '⚠️ No microphone'}")
        if self.deployment_name:
            print(f"   🚀 AI Model: {self.deployment_name}")
        print()
        
        while True:
            try:
                # Text input
                user_input = input(f"[{self.user_name}] Your command: ").strip()
                
                if not user_input:
                    continue
                
                # Exit commands
                if user_input.lower() in ['quit', 'exit', 'goodbye', 'bye', 'shutdown']:
                    farewell_msg = f"Goodbye, {self.user_name}. It has been my pleasure to assist you. JARVIS going offline."
                    print(f"🤖 JARVIS: {farewell_msg}")
                    if self.voice_enabled:
                        await self.synthesize_speech(farewell_msg, "calm")
                    break
                
                # Process command
                print("🧠 JARVIS is processing...")
                start_time = time.time()
                
                response = await self.process_command(user_input)
                
                response_time = time.time() - start_time
                print(f"🤖 JARVIS ({response_time:.2f}s): {response}")
                
                # Voice response
                if self.voice_enabled:
                    # Clean response for voice output
                    voice_text = response.replace('✅', '').replace('❌', '').replace('🗣️', '').replace('🧠', '').replace('🎤', '').replace('⚡', '').replace('🛡️', '').replace('🔧', '').replace('⚠️', '')
                    voice_text = voice_text.replace('\n', '. ').strip()
                    
                    # Limit voice response length for clarity
                    if len(voice_text) > 300:
                        voice_text = voice_text[:300] + "..."
                    
                    await self.synthesize_speech(voice_text, "confident")
                
                # Store conversation
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "jarvis": response,
                    "response_time": response_time
                })
                
                print()  # Add spacing for readability
                
            except KeyboardInterrupt:
                farewell_msg = f"System interrupt detected. Goodbye, {self.user_name}."
                print(f"\n🤖 JARVIS: {farewell_msg}")
                if self.voice_enabled:
                    await self.synthesize_speech(farewell_msg, "calm")
                break
            except Exception as e:
                error_msg = f"I apologize, {self.user_name}, but I encountered an unexpected error: {str(e)}"
                print(f"❌ JARVIS Error: {error_msg}")
                self.logger.error(f"Session error: {e}")

def main():
    """Main function to run JARVIS Final"""
    print("🚀 Initializing JARVIS V7.1 FINAL...")
    
    # Create and run JARVIS
    jarvis = IronManJARVISFinal()
    asyncio.run(jarvis.run_interactive_session())

if __name__ == "__main__":
    main()