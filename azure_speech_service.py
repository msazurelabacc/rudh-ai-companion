# azure_speech_service.py
"""
Azure Speech Services Integration for Rudh
WORKING VERSION - Simple text synthesis without complex SSML
"""

import asyncio
import logging
import os
import tempfile
from typing import Dict, Optional, Any
from datetime import datetime

# Import existing config
import sys
sys.path.append('src')
from config.config import RudhConfig

# Graceful imports with fallbacks
try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SPEECH_AVAILABLE = True
except ImportError:
    AZURE_SPEECH_AVAILABLE = False
    speechsdk = None

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    def load_dotenv():
        pass

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

# Calculate overall speech availability
SPEECH_AVAILABLE = AZURE_SPEECH_AVAILABLE and PYGAME_AVAILABLE

class AzureSpeechService:
    """Azure Speech Services for Rudh AI Companion - Simple Working Version"""
    
    def __init__(self):
        # Load environment variables if available
        if DOTENV_AVAILABLE:
            load_dotenv()
        
        self.config = RudhConfig.get_config()
        self.speech_config = self.config['azure']['speech']
        self.speech_client = None
        self.is_available = SPEECH_AVAILABLE
        self.speech_connected = False
        self.logger = logging.getLogger("AzureSpeechService")
        
        # Initialize pygame mixer for audio playback if available
        if self.is_available:
            try:
                pygame.mixer.init()
                self._initialize_speech_client()
            except Exception as e:
                self.logger.error(f"Speech service initialization failed: {e}")
                self.is_available = False
        
        # Log availability status
        self._log_availability_status()
    
    def _log_availability_status(self):
        """Log the availability status of dependencies"""
        self.logger.info("🔍 Speech Service Dependency Check:")
        self.logger.info(f"   Azure Speech SDK: {'✅' if AZURE_SPEECH_AVAILABLE else '❌'}")
        self.logger.info(f"   Pygame Audio: {'✅' if PYGAME_AVAILABLE else '❌'}")
        self.logger.info(f"   Python-dotenv: {'✅' if DOTENV_AVAILABLE else '❌'}")
        self.logger.info(f"   Overall Available: {'✅' if self.is_available else '🔧 Fallback Mode'}")
    
    def _initialize_speech_client(self):
        """Initialize Azure Speech client"""
        try:
            speech_key = os.getenv('AZURE_SPEECH_KEY')
            speech_region = os.getenv('AZURE_SPEECH_REGION', 'southeastasia')
            
            if not speech_key:
                self.logger.warning("Azure Speech key not found in environment")
                return
            
            # Create speech config
            self.speech_config_sdk = speechsdk.SpeechConfig(
                subscription=speech_key, 
                region=speech_region
            )
            
            # Set voice (Indian English female voice)
            voice_name = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
            self.speech_config_sdk.speech_synthesis_voice_name = voice_name
            
            # Set audio format for better quality
            self.speech_config_sdk.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
            )
            
            self.speech_connected = True
            self.logger.info(f"✅ Azure Speech client initialized with voice: {voice_name}")
            
        except Exception as e:
            self.logger.error(f"Speech client initialization failed: {e}")
            self.speech_connected = False
    
    async def text_to_speech(self, text: str, emotion: str = "neutral") -> Dict[str, Any]:
        """Convert text to speech - SIMPLE VERSION without complex SSML"""
        start_time = datetime.now()
        
        try:
            if not self.speech_connected or not self.speech_config_sdk:
                return self._fallback_response(text, start_time)
            
            # Create synthesizer with default audio config (let Azure handle it)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config_sdk,
                audio_config=None  # Let Azure SDK handle audio automatically
            )
            
            # SIMPLE APPROACH: Use plain text instead of complex SSML
            # This avoids the SPXERR_INVALID_ARG error
            result = synthesizer.speak_text_async(text).get()
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                self.logger.info(f"✅ Speech synthesis successful: {len(result.audio_data)} bytes")
                
                return {
                    "success": True,
                    "audio_file": None,  # Audio played directly via Azure SDK
                    "text": text,
                    "voice": self.speech_config_sdk.speech_synthesis_voice_name,
                    "emotion": emotion,
                    "processing_time": f"{processing_time:.3f}s",
                    "audio_length": len(result.audio_data),
                    "source": "azure_speech_simple",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.logger.error(f"Speech synthesis failed: {result.reason}")
                if result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = speechsdk.CancellationDetails(result)
                    self.logger.error(f"Cancellation reason: {cancellation_details.reason}")
                    if cancellation_details.error_details:
                        self.logger.error(f"Error details: {cancellation_details.error_details}")
                return self._fallback_response(text, start_time)
                
        except Exception as e:
            self.logger.error(f"Text-to-speech failed: {e}")
            return self._fallback_response(text, start_time)
    
    async def speak_text(self, text: str, emotion: str = "neutral") -> bool:
        """Complete text-to-speech pipeline: synthesize and play directly"""
        try:
            if not self.is_available:
                print("🔧 Speech synthesis unavailable - text response only")
                return False
            
            # Clean text for speech (remove emojis and special characters)
            clean_text = self._clean_text_for_speech(text)
            
            # Generate and play speech directly
            speech_result = await self.text_to_speech(clean_text, emotion)
            
            if not speech_result["success"]:
                print("🔧 Speech synthesis failed - text response only")
                return False
            
            print(f"🎵 Speaking with {speech_result['voice']} voice...")
            print(f"✅ Speech completed ({speech_result['processing_time']})")
            return True
                
        except Exception as e:
            self.logger.error(f"Speak text failed: {e}")
            return False
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text for speech synthesis"""
        import re
        
        # Remove emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub('', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Limit length for better speech quality
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text.strip()
    
    def _fallback_response(self, text: str, start_time: datetime) -> Dict[str, Any]:
        """Fallback response when speech unavailable"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": False,
            "audio_file": None,
            "text": text,
            "voice": "text_only",
            "emotion": "neutral",
            "processing_time": f"{processing_time:.3f}s",
            "audio_length": 0,
            "source": "fallback_mode",
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get speech service status"""
        return {
            "speech_sdk_available": AZURE_SPEECH_AVAILABLE,
            "speech_connected": self.speech_connected,
            "pygame_available": PYGAME_AVAILABLE if PYGAME_AVAILABLE else False,
            "dotenv_available": DOTENV_AVAILABLE,
            "overall_available": self.is_available,
            "voice": self.speech_config_sdk.speech_synthesis_voice_name if self.speech_connected else "not_configured",
            "region": os.getenv('AZURE_SPEECH_REGION', 'not_configured'),
            "fallback_mode": not self.speech_connected,
            "missing_dependencies": self._get_missing_dependencies(),
            "synthesis_method": "simple_text",  # No complex SSML
            "last_check": datetime.now().isoformat()
        }
    
    def _get_missing_dependencies(self) -> list:
        """Get list of missing dependencies"""
        missing = []
        if not AZURE_SPEECH_AVAILABLE:
            missing.append("azure-cognitiveservices-speech")
        if not PYGAME_AVAILABLE:
            missing.append("pygame")
        if not DOTENV_AVAILABLE:
            missing.append("python-dotenv")
        return missing
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if PYGAME_AVAILABLE and pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")

# Test function
async def test_speech_service():
    """Test the speech service with simple approach"""
    print("🧪 Testing Azure Speech Service (Simple Version)...")
    print("=" * 60)
    
    service = AzureSpeechService()
    
    # Check status
    status = await service.get_service_status()
    print(f"📊 SERVICE STATUS:")
    print(f"   Azure Speech SDK: {'✅' if status['speech_sdk_available'] else '❌'}")
    print(f"   Speech Connected: {'✅' if status['speech_connected'] else '🔧'}")
    print(f"   Synthesis Method: {status['synthesis_method']}")
    print(f"   Overall Status: {'✅ READY' if status['overall_available'] else '🔧 FALLBACK'}")
    
    if status['speech_connected']:
        print(f"\n✅ Testing simple speech synthesis...")
        print(f"   Voice: {status['voice']}")
        print(f"   Region: {status['region']}")
        
        # Test simple phrases
        test_phrases = [
            "Hello! I'm Rudh, your AI companion.",
            "I understand you're feeling frustrated.",
            "That's wonderful news! I'm excited for you!"
        ]
        
        for i, text in enumerate(test_phrases, 1):
            print(f"\n🎵 Test {i}: '{text}'...")
            success = await service.speak_text(text, "neutral")
            if success:
                print("✅ Speech test successful!")
            else:
                print("❌ Speech test failed")
    else:
        print(f"\n🔧 Speech service in fallback mode")
    
    print(f"\n🎯 READY FOR RUDH INTEGRATION!")
    service.cleanup()

if __name__ == "__main__":
    asyncio.run(test_speech_service())