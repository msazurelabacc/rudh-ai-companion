# azure_speech_service_v44.py
"""
Azure Speech Services V4.4 - Professional Voice Integration for Rudh
Indian English voice synthesis with emotional styling and Chennai context
"""

import asyncio
import logging
import os
import tempfile
import wave
from typing import Dict, Optional, Any, List
from datetime import datetime
from pathlib import Path

try:
    import azure.cognitiveservices.speech as speechsdk
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class AzureSpeechService:
    """Professional Azure Speech Services Integration for Rudh"""
    
    def __init__(self):
        self.setup_logging()
        
        # Service availability
        self.is_available = SPEECH_AVAILABLE
        self.speech_connected = False
        self.speech_config_sdk = None
        
        # Voice configuration
        self.voice_personas = {
            'professional': {
                'voice': 'en-IN-NeerjaNeural',
                'style': 'newscast',
                'rate': '0%',
                'pitch': '0%'
            },
            'enthusiastic': {
                'voice': 'en-IN-NeerjaNeural',
                'style': 'cheerful',
                'rate': '+10%',
                'pitch': '+5%'
            },
            'authoritative': {
                'voice': 'en-IN-PrabhatNeural',
                'style': 'newscast',
                'rate': '-5%',
                'pitch': '-5%'
            },
            'friendly': {
                'voice': 'en-IN-NeerjaNeural',
                'style': 'friendly',
                'rate': '0%',
                'pitch': '0%'
            },
            'tamil_friendly': {
                'voice': 'ta-IN-PallaviNeural',
                'style': 'friendly',
                'rate': '0%',
                'pitch': '0%'
            }
        }
        
        # Audio settings
        self.audio_dir = Path("audio_output")
        self.audio_dir.mkdir(exist_ok=True)
        
        # Initialize services
        if self.is_available:
            self._initialize_speech_client()
            if PYGAME_AVAILABLE:
                pygame.mixer.init()
        
        self.log_status()
    
    def setup_logging(self):
        """Setup logging"""
        self.logger = logging.getLogger('AzureSpeechService')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_status(self):
        """Log service status"""
        self.logger.info("🗣️ Azure Speech Service V4.4 Status:")
        self.logger.info(f"   Azure Speech SDK: {'✅' if SPEECH_AVAILABLE else '❌'}")
        self.logger.info(f"   Pygame Audio: {'✅' if PYGAME_AVAILABLE else '❌'}")
        self.logger.info(f"   Python-dotenv: {'✅' if DOTENV_AVAILABLE else '❌'}")
        self.logger.info(f"   Speech Connected: {'✅' if self.speech_connected else '❌'}")
        self.logger.info(f"   Overall Available: {'✅' if self.speech_connected else '🔧 Fallback Mode'}")
    
    def _initialize_speech_client(self):
        """Initialize Azure Speech client"""
        try:
            # Try multiple methods to get credentials
            speech_key, speech_region = self._get_azure_credentials()
            
            if not speech_key:
                self.logger.warning("⚠️ Azure Speech credentials not available")
                return
            
            # Create speech config
            self.speech_config_sdk = speechsdk.SpeechConfig(
                subscription=speech_key, 
                region=speech_region
            )
            
            # Set default voice (Indian English female)
            default_voice = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
            self.speech_config_sdk.speech_synthesis_voice_name = default_voice
            
            # Set high-quality audio format
            self.speech_config_sdk.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
            )
            
            self.speech_connected = True
            self.logger.info(f"✅ Azure Speech client initialized with voice: {default_voice}")
            
        except Exception as e:
            self.logger.error(f"❌ Speech client initialization failed: {e}")
            self.speech_connected = False
    
    def _get_azure_credentials(self) -> tuple:
        """Get Azure credentials from multiple sources"""
        # Method 1: Environment variables
        speech_key = os.getenv('AZURE_SPEECH_KEY')
        speech_region = os.getenv('AZURE_SPEECH_REGION', 'eastus2')
        
        if speech_key:
            self.logger.info("✅ Using speech credentials from environment")
            return speech_key, speech_region
        
        # Method 2: Key Vault (if available)
        try:
            key_vault_url = os.getenv('AZURE_KEY_VAULT_URL', 
                                    'https://kv-rudh-secrets-eastus2.vault.azure.net/')
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=key_vault_url, credential=credential)
            
            speech_key = client.get_secret('rudh-speech-key').value
            speech_region = client.get_secret('rudh-speech-region').value
            
            self.logger.info("✅ Using speech credentials from Key Vault")
            return speech_key, speech_region
            
        except Exception as e:
            self.logger.warning(f"⚠️ Key Vault access failed: {e}")
        
        # Method 3: Fallback values for testing
        self.logger.warning("⚠️ Using fallback test credentials")
        return None, 'eastus2'
    
    async def text_to_speech_with_persona(self, text: str, persona: str = "professional", 
                                        save_to_file: bool = True) -> Dict[str, Any]:
        """Convert text to speech with voice persona and emotional styling"""
        start_time = datetime.now()
        
        try:
            if not self.speech_connected or not self.speech_config_sdk:
                return self._fallback_response(text, start_time)
            
            # Get persona configuration
            persona_config = self.voice_personas.get(persona, self.voice_personas['professional'])
            
            # Create SSML with emotional styling
            ssml_text = self._create_ssml(text, persona_config)
            
            # Configure synthesizer
            audio_filename = None
            if save_to_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_filename = self.audio_dir / f"voice_{persona}_{timestamp}.wav"
                audio_config = speechsdk.audio.AudioOutputConfig(filename=str(audio_filename))
            else:
                audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config_sdk,
                audio_config=audio_config
            )
            
            # Synthesize speech
            result = synthesizer.speak_ssml_async(ssml_text).get()
            
            # Check result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                duration = (datetime.now() - start_time).total_seconds()
                
                file_size = 0
                if save_to_file and audio_filename and audio_filename.exists():
                    file_size = audio_filename.stat().st_size
                
                self.logger.info(f"✅ Voice synthesis successful: {persona} persona")
                self.logger.info(f"   Duration: {duration:.2f}s, Size: {file_size} bytes")
                
                return {
                    'success': True,
                    'audio_file': str(audio_filename) if audio_filename else None,
                    'duration': duration,
                    'file_size': file_size,
                    'persona': persona,
                    'voice': persona_config['voice'],
                    'text_length': len(text),
                    'timestamp': start_time.isoformat()
                }
            
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                self.logger.error(f"❌ Speech synthesis canceled: {cancellation.reason}")
                if cancellation.error_details:
                    self.logger.error(f"   Error: {cancellation.error_details}")
                
                return self._fallback_response(text, start_time, error=str(cancellation.reason))
            
        except Exception as e:
            self.logger.error(f"❌ Speech synthesis failed: {e}")
            return self._fallback_response(text, start_time, error=str(e))
    
    def _create_ssml(self, text: str, persona_config: Dict) -> str:
        """Create SSML markup for enhanced voice styling"""
        voice = persona_config['voice']
        style = persona_config.get('style', 'friendly')
        rate = persona_config.get('rate', '0%')
        pitch = persona_config.get('pitch', '0%')
        
        # Clean text for SSML
        clean_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Create SSML with emotional styling
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
               xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-IN">
            <voice name="{voice}">
                <mstts:express-as style="{style}">
                    <prosody rate="{rate}" pitch="{pitch}">
                        {clean_text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """
        return ssml.strip()
    
    def _fallback_response(self, text: str, start_time: datetime, error: str = None) -> Dict[str, Any]:
        """Create fallback response when speech synthesis fails"""
        duration = (datetime.now() - start_time).total_seconds()
        
        return {
            'success': False,
            'audio_file': None,
            'duration': duration,
            'file_size': 0,
            'persona': 'fallback',
            'voice': 'text-only',
            'text_length': len(text),
            'timestamp': start_time.isoformat(),
            'error': error or 'Speech services not available',
            'fallback_text': text
        }
    
    async def create_video_narration(self, video_script: Dict, persona: str = "professional") -> Dict[str, Any]:
        """Create voice narration for video scripts"""
        self.logger.info(f"🎬 Creating video narration with {persona} persona")
        
        narration_files = []
        total_duration = 0
        
        try:
            scenes = video_script.get('scenes', [])
            
            for i, scene in enumerate(scenes):
                narration_text = scene.get('narration', '')
                if not narration_text:
                    continue
                
                self.logger.info(f"📝 Scene {i+1}: Generating narration...")
                
                # Generate voice for this scene
                result = await self.text_to_speech_with_persona(
                    narration_text, persona, save_to_file=True
                )
                
                if result['success']:
                    narration_files.append({
                        'scene': i+1,
                        'audio_file': result['audio_file'],
                        'duration': result['duration'],
                        'text': narration_text
                    })
                    total_duration += result['duration']
                else:
                    self.logger.warning(f"⚠️ Scene {i+1} narration failed, skipping")
            
            return {
                'success': True,
                'narration_files': narration_files,
                'total_scenes': len(scenes),
                'completed_scenes': len(narration_files),
                'total_duration': total_duration,
                'persona': persona
            }
            
        except Exception as e:
            self.logger.error(f"❌ Video narration creation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'narration_files': narration_files,
                'total_duration': total_duration
            }
    
    def play_audio(self, audio_file: str) -> bool:
        """Play audio file using pygame"""
        try:
            if not PYGAME_AVAILABLE:
                self.logger.warning("⚠️ Pygame not available for audio playback")
                return False
            
            if not os.path.exists(audio_file):
                self.logger.error(f"❌ Audio file not found: {audio_file}")
                return False
            
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            self.logger.info(f"🔊 Playing audio: {os.path.basename(audio_file)}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Audio playback failed: {e}")
            return False
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available voice personas"""
        return [
            {
                'persona': 'professional',
                'description': 'Professional business tone, perfect for presentations',
                'voice': 'en-IN-NeerjaNeural (Female)',
                'language': 'Indian English',
                'recommended_for': 'Business presentations, formal content'
            },
            {
                'persona': 'enthusiastic',
                'description': 'Energetic and engaging, great for marketing content',
                'voice': 'en-IN-NeerjaNeural (Female)',
                'language': 'Indian English',
                'recommended_for': 'Marketing videos, social media content'
            },
            {
                'persona': 'authoritative',
                'description': 'Confident and credible, ideal for educational content',
                'voice': 'en-IN-PrabhatNeural (Male)',
                'language': 'Indian English',
                'recommended_for': 'Educational videos, expert explanations'
            },
            {
                'persona': 'friendly',
                'description': 'Warm and approachable, perfect for tutorials',
                'voice': 'en-IN-NeerjaNeural (Female)',
                'language': 'Indian English',
                'recommended_for': 'Tutorials, how-to videos'
            },
            {
                'persona': 'tamil_friendly',
                'description': 'Tamil voice for cultural authenticity',
                'voice': 'ta-IN-PallaviNeural (Female)',
                'language': 'Tamil',
                'recommended_for': 'Local Tamil Nadu content'
            }
        ]
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get comprehensive service status"""
        return {
            'speech_available': SPEECH_AVAILABLE,
            'pygame_available': PYGAME_AVAILABLE,
            'dotenv_available': DOTENV_AVAILABLE,
            'speech_connected': self.speech_connected,
            'overall_status': 'operational' if self.speech_connected else 'fallback',
            'available_personas': list(self.voice_personas.keys()),
            'audio_output_dir': str(self.audio_dir),
            'features': [
                'Indian English voice synthesis',
                'Tamil language support',
                'Multiple voice personas',
                'Emotional voice styling',
                'Video narration creation',
                'SSML advanced markup',
                'High-quality audio export'
            ]
        }

# Test function
async def test_azure_speech_service():
    """Test Azure Speech Service functionality"""
    print("🧪 Testing Azure Speech Service V4.4")
    print("=" * 50)
    
    service = AzureSpeechService()
    
    # Test status
    print("\n📊 Service Status:")
    status = service.get_service_status()
    for key, value in status.items():
        if key not in ['features', 'available_personas']:
            print(f"   {'✅' if value else '❌'} {key}: {value}")
    
    print(f"\n🗣️ Available Personas: {', '.join(status['available_personas'])}")
    
    print("\n🎵 Available Features:")
    for feature in status['features']:
        print(f"   ✅ {feature}")
    
    # Test voice synthesis
    if service.speech_connected:
        print("\n🎬 Testing Voice Synthesis:")
        
        test_text = "Welcome to Rudh's enhanced video creation system with professional Indian English narration."
        
        result = await service.text_to_speech_with_persona(
            test_text, 
            persona="professional"
        )
        
        if result['success']:
            print(f"   ✅ Voice synthesis successful!")
            print(f"   📊 Duration: {result['duration']:.2f}s")
            print(f"   📁 Audio file: {result['audio_file']}")
            print(f"   🗣️ Voice: {result['voice']}")
            print(f"   📝 Text length: {result['text_length']} characters")
            
            # Test playback
            if result['audio_file']:
                print("\n🔊 Testing Audio Playback:")
                playback_success = service.play_audio(result['audio_file'])
                if playback_success:
                    print("   ✅ Audio playback successful!")
                else:
                    print("   ⚠️ Audio playback not available")
        else:
            print(f"   ⚠️ Voice synthesis using fallback mode")
            print(f"   📝 Fallback text: {result.get('fallback_text', 'N/A')}")
    
    else:
        print("\n⚠️ Speech services not connected - running in fallback mode")
    
    return service

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_azure_speech_service())