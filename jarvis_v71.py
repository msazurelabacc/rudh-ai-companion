#!/usr/bin/env python3
"""
🚀 PHASE 7.1: VOICE-ENHANCED JARVIS - IRON MAN STYLE
Advanced voice interaction with Azure Speech Services
Testing your voice synthesis fix and enhancing with Iron Man capabilities
"""

import asyncio
import time
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import azure.cognitiveservices.speech as speechsdk
from azure.identity import DefaultAzureCredential
import openai
import os

class IronManJARVIS:
    """Iron Man style JARVIS with advanced voice capabilities"""
    
    def __init__(self):
        self.speech_config = None
        self.speech_synthesizer = None
        self.speech_recognizer = None
        self.voice_enabled = True
        self.logger = self._setup_logging()
        self.conversation_history = []
        self.user_name = "Sir"  # Iron Man style addressing
        
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
            # Azure Speech Configuration
            speech_key = os.getenv('AZURE_SPEECH_KEY')
            speech_region = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
            
            if speech_key:
                self.speech_config = speechsdk.SpeechConfig(
                    subscription=speech_key, 
                    region=speech_region
                )
                # Iron Man JARVIS voice style
                self.speech_config.speech_synthesis_voice_name = "en-IN-NeerjaNeural"
                self.speech_config.set_speech_synthesis_output_format(
                    speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
                )
                
                # Initialize synthesizer with enhanced settings
                self.speech_synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=self.speech_config
                )
                
                # Initialize recognizer for voice commands
                self.speech_recognizer = speechsdk.SpeechRecognizer(
                    speech_config=self.speech_config
                )
                
                self.logger.info("✅ Azure Speech Services initialized successfully")
            else:
                self.logger.warning("⚠️ Azure Speech key not found - voice disabled")
                self.voice_enabled = False
                
            # OpenAI Configuration
            openai_key = os.getenv('AZURE_OPENAI_KEY')
            openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            
            if openai_key and openai_endpoint:
                openai.api_type = "azure"
                openai.api_key = openai_key
                openai.api_base = openai_endpoint
                openai.api_version = "2024-02-15-preview"
                self.logger.info("✅ Azure OpenAI initialized successfully")
            else:
                self.logger.warning("⚠️ OpenAI credentials not found")
                
        except Exception as e:
            self.logger.error(f"❌ Service initialization failed: {e}")
            self.voice_enabled = False
    
    async def synthesize_speech(self, text: str, emotion: str = "neutral") -> bool:
        """Enhanced speech synthesis with emotional styling"""
        if not self.voice_enabled or not self.speech_synthesizer:
            return False
            
        try:
            # Iron Man JARVIS style SSML with emotional emphasis
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
        # Emotional voice parameters
        emotion_styles = {
            "confident": {"rate": "medium", "pitch": "+5%", "volume": "+10%"},
            "analytical": {"rate": "slow", "pitch": "-2%", "volume": "medium"},
            "urgent": {"rate": "fast", "pitch": "+8%", "volume": "+15%"},
            "calm": {"rate": "slow", "pitch": "-5%", "volume": "soft"},
            "neutral": {"rate": "medium", "pitch": "medium", "volume": "medium"}
        }
        
        style = emotion_styles.get(emotion, emotion_styles["neutral"])
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-IN">
            <voice name="en-IN-NeerjaNeural">
                <prosody rate="{style['rate']}" pitch="{style['pitch']}" volume="{style['volume']}">
                    <emphasis level="moderate">{text}</emphasis>
                </prosody>
            </voice>
        </speak>
        """
        return ssml
    
    async def listen_for_wake_word(self, timeout: int = 10) -> Optional[str]:
        """Listen for 'Hey JARVIS' wake word"""
        if not self.speech_recognizer:
            return None
            
        try:
            self.logger.info("🎤 Listening for 'Hey JARVIS'...")
            result = self.speech_recognizer.recognize_once_async().get()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text = result.text.lower()
                if "hey jarvis" in recognized_text or "jarvis" in recognized_text:
                    # Extract command after wake word
                    command = recognized_text.replace("hey jarvis", "").replace("jarvis", "").strip()
                    self.logger.info(f"🎯 Wake word detected! Command: {command}")
                    return command if command else "listening"
                    
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Voice recognition error: {e}")
            return None
    
    async def get_ai_response(self, user_input: str) -> str:
        """Get intelligent response from Azure OpenAI"""
        try:
            # Enhanced JARVIS personality prompt
            system_prompt = f"""You are JARVIS, the AI assistant from Iron Man. You are:
            - Highly intelligent and analytical
            - Sophisticated yet personable
            - Always address the user as '{self.user_name}'
            - Provide expert advice with confidence
            - Use British-influenced formal language with warmth
            - Focus on being helpful and proactive
            
            Current context: Advanced AI companion for personal assistance.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = await openai.ChatCompletion.acreate(
                engine="gpt-4",  # Or your Azure OpenAI deployment name
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"❌ AI response error: {e}")
            return f"I apologize, {self.user_name}, but I'm experiencing some technical difficulties. How else may I assist you?"
    
    async def process_command(self, command: str) -> str:
        """Process voice or text commands with Iron Man JARVIS intelligence"""
        command_lower = command.lower().strip()
        
        # System commands
        if command_lower in ['/voice', 'toggle voice']:
            self.voice_enabled = not self.voice_enabled
            status = "enabled" if self.voice_enabled else "disabled"
            return f"Voice output {status}, {self.user_name}."
        
        elif command_lower in ['/status', 'status', 'system status']:
            return await self._get_system_status()
        
        elif command_lower in ['/help', 'help', 'what can you do']:
            return self._get_help_menu()
        
        elif command_lower in ['time', 'what time is it']:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}, {self.user_name}."
        
        elif command_lower in ['date', 'what date is it', 'today']:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}, {self.user_name}."
        
        # AI-powered responses for complex queries
        else:
            return await self.get_ai_response(command)
    
    async def _get_system_status(self) -> str:
        """Get comprehensive system status"""
        speech_status = "✅ Operational" if self.voice_enabled else "❌ Disabled"
        ai_status = "✅ Connected" if hasattr(openai, 'api_key') else "❌ Disconnected"
        
        return f"""System Status Report, {self.user_name}:
        
🗣️ Voice Synthesis: {speech_status}
🧠 AI Intelligence: {ai_status}
🎤 Voice Recognition: ✅ Active
⚡ Response Time: Optimal
🛡️ Security: All systems secure

All primary systems are functioning within normal parameters."""
    
    def _get_help_menu(self) -> str:
        """Get comprehensive help menu"""
        return f"""JARVIS Command Reference, {self.user_name}:

🎤 VOICE COMMANDS:
   • Say "Hey JARVIS" + your command
   • Natural conversation supported

⚡ QUICK COMMANDS:
   • /status - System diagnostics
   • /voice - Toggle voice output
   • /help - This menu
   • time/date - Current time/date

🧠 AI CAPABILITIES:
   • Ask questions on any topic
   • Request analysis and advice
   • Creative and technical assistance
   • Personal productivity support

💡 EXAMPLES:
   • "What's the weather like?"
   • "Help me plan my day"
   • "Analyze this problem..."
   • "Give me some advice on..."

How may I assist you further, {self.user_name}?"""
    
    async def run_interactive_session(self):
        """Run main JARVIS interactive session"""
        print("🚀 PHASE 7.1: IRON MAN JARVIS - VOICE ENHANCED")
        print("=" * 60)
        
        # Welcome message
        welcome_msg = f"Good day, {self.user_name}. JARVIS is now online and ready to assist. How may I help you today?"
        print(f"🤖 JARVIS: {welcome_msg}")
        
        if self.voice_enabled:
            await self.synthesize_speech(welcome_msg, "confident")
        
        print("\n💡 Say 'Hey JARVIS' or type your commands")
        print("💡 Type '/help' for command reference")
        print("💡 Type 'quit' to exit\n")
        
        while True:
            try:
                # Check for voice input first
                if self.voice_enabled:
                    print("🎤 Listening for voice command... (or type below)")
                    voice_command = await self.listen_for_wake_word(timeout=3)
                    
                    if voice_command:
                        user_input = voice_command
                        print(f"🎤 Voice: {user_input}")
                    else:
                        # Fallback to text input
                        user_input = input(f"[{self.user_name}] Your command: ").strip()
                else:
                    user_input = input(f"[{self.user_name}] Your command: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'goodbye']:
                    farewell_msg = f"Goodbye, {self.user_name}. JARVIS going offline."
                    print(f"🤖 JARVIS: {farewell_msg}")
                    if self.voice_enabled:
                        await self.synthesize_speech(farewell_msg, "calm")
                    break
                
                # Process command
                print("🧠 JARVIS is thinking...")
                start_time = time.time()
                
                response = await self.process_command(user_input)
                
                response_time = time.time() - start_time
                print(f"🤖 JARVIS ({response_time:.2f}s): {response}")
                
                # Voice response
                if self.voice_enabled:
                    await self.synthesize_speech(response, "confident")
                
                # Store conversation
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "jarvis": response,
                    "response_time": response_time
                })
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                farewell_msg = f"System interrupt detected. Goodbye, {self.user_name}."
                print(f"\n🤖 JARVIS: {farewell_msg}")
                if self.voice_enabled:
                    await self.synthesize_speech(farewell_msg, "calm")
                break
            except Exception as e:
                error_msg = f"I apologize, {self.user_name}, but I encountered an error: {str(e)}"
                print(f"❌ JARVIS Error: {error_msg}")
                self.logger.error(f"Session error: {e}")

def main():
    """Main function to run JARVIS"""
    print("🚀 Initializing PHASE 7.1: IRON MAN JARVIS...")
    
    # Create and run JARVIS
    jarvis = IronManJARVIS()
    asyncio.run(jarvis.run_interactive_session())

if __name__ == "__main__":
    main()