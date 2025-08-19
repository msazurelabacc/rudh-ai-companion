# src/azure_integration/azure_services.py
"""
Rudh AI Azure Services Integration - Phase 2.3
Production-grade Azure AI services integration for Rudh
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Azure SDK imports with fallbacks
try:
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    from azure.keyvault.secrets import SecretClient
    from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
    from azure.ai.translation.text import TextTranslationClient
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import VectorizedQuery
    import openai
    AZURE_SDK_AVAILABLE = True
except ImportError as e:
    print(f"Azure SDK not available: {e}")
    AZURE_SDK_AVAILABLE = False

@dataclass
class AzureServiceConfig:
    """Configuration for Azure services"""
    subscription_id: str
    resource_group: str
    region: str
    key_vault_name: str
    openai_endpoint: str
    openai_deployment_name: str
    speech_key: str
    speech_region: str
    translator_key: str
    search_endpoint: str
    search_key: str

class AzureCredentialManager:
    """Secure credential management using Azure Key Vault"""
    
    def __init__(self, key_vault_url: str):
        self.key_vault_url = key_vault_url
        self.credential = None
        self.secret_client = None
        self.logger = logging.getLogger('AzureCredentials')
        
    async def initialize(self) -> bool:
        """Initialize Azure credentials securely"""
        try:
            if not AZURE_SDK_AVAILABLE:
                self.logger.error("Azure SDK not available")
                return False
                
            # Use Managed Identity in production, DefaultAzureCredential for development
            self.credential = DefaultAzureCredential()
            
            # Initialize Key Vault client
            self.secret_client = SecretClient(
                vault_url=self.key_vault_url,
                credential=self.credential
            )
            
            # Test credential access
            await self._test_key_vault_access()
            
            self.logger.info("Azure credentials initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure credentials: {e}")
            return False
    
    async def get_secret(self, secret_name: str) -> Optional[str]:
        """Securely retrieve secret from Key Vault"""
        try:
            if not self.secret_client:
                await self.initialize()
                
            secret = await self.secret_client.get_secret(secret_name)
            return secret.value
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            return None
    
    async def _test_key_vault_access(self):
        """Test Key Vault connectivity"""
        try:
            # Try to list secrets (metadata only)
            secrets = self.secret_client.list_properties_of_secrets()
            secret_count = len(list(secrets))
            self.logger.info(f"Key Vault access confirmed. {secret_count} secrets available.")
        except Exception as e:
            raise Exception(f"Key Vault access test failed: {e}")

class RudhAzureOpenAI:
    """Enhanced Azure OpenAI integration for Rudh"""
    
    def __init__(self, credential_manager: AzureCredentialManager):
        self.credential_manager = credential_manager
        self.client = None
        self.deployment_name = None
        self.logger = logging.getLogger('RudhAzureOpenAI')
        
    async def initialize(self, endpoint: str, deployment_name: str) -> bool:
        """Initialize Azure OpenAI client"""
        try:
            # Get API key from Key Vault
            api_key = await self.credential_manager.get_secret("rudh-openai-key")
            if not api_key:
                self.logger.error("Failed to retrieve OpenAI API key")
                return False
                
            # Initialize OpenAI client
            self.client = openai.AzureOpenAI(
                api_key=api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=endpoint
            )
            
            self.deployment_name = deployment_name
            
            # Test connectivity
            await self._test_openai_connection()
            
            self.logger.info("Azure OpenAI initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure OpenAI: {e}")
            return False
    
    async def generate_response(self, messages: List[Dict], **kwargs) -> Dict:
        """Generate response using Azure OpenAI"""
        try:
            if not self.client:
                raise Exception("Azure OpenAI not initialized")
                
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', 800),
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 0.9),
                frequency_penalty=kwargs.get('frequency_penalty', 0.1),
                presence_penalty=kwargs.get('presence_penalty', 0.1)
            )
            
            return {
                'content': response.choices[0].message.content,
                'usage': response.usage,
                'model': response.model,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"OpenAI generation failed: {e}")
            raise
    
    async def _test_openai_connection(self):
        """Test OpenAI connectivity"""
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        
        response = await self.generate_response(test_messages, max_tokens=10)
        if response and 'content' in response:
            self.logger.info("OpenAI connection test successful")
        else:
            raise Exception("OpenAI connection test failed")

class RudhSpeechServices:
    """Azure Speech Services integration for voice capabilities"""
    
    def __init__(self, credential_manager: AzureCredentialManager):
        self.credential_manager = credential_manager
        self.speech_config = None
        self.synthesizer = None
        self.logger = logging.getLogger('RudhSpeech')
        
    async def initialize(self, region: str) -> bool:
        """Initialize Speech Services"""
        try:
            # Get Speech key from Key Vault
            speech_key = await self.credential_manager.get_secret("rudh-speech-key")
            if not speech_key:
                self.logger.error("Failed to retrieve Speech API key")
                return False
                
            # Configure Speech Services
            self.speech_config = SpeechConfig(
                subscription=speech_key,
                region=region
            )
            
            # Configure voice for Rudh (warm, professional)
            self.speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"  # Indian English voice
            
            # Initialize synthesizer
            self.synthesizer = SpeechSynthesizer(speech_config=self.speech_config)
            
            # Test synthesis
            await self._test_speech_synthesis()
            
            self.logger.info("Speech Services initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Speech Services: {e}")
            return False
    
    async def synthesize_speech(self, text: str, voice_style: str = "friendly") -> bytes:
        """Convert text to speech with emotional styling"""
        try:
            if not self.synthesizer:
                raise Exception("Speech Services not initialized")
                
            # Enhanced SSML for emotional expression
            ssml_text = self._create_emotional_ssml(text, voice_style)
            
            # Synthesize speech
            result = self.synthesizer.speak_ssml_async(ssml_text).get()
            
            if result.reason.name == 'SynthesizingAudioCompleted':
                return result.audio_data
            else:
                raise Exception(f"Speech synthesis failed: {result.reason}")
                
        except Exception as e:
            self.logger.error(f"Speech synthesis failed: {e}")
            raise
    
    def _create_emotional_ssml(self, text: str, style: str) -> str:
        """Create SSML with emotional styling"""
        style_map = {
            'friendly': 'friendly',
            'empathetic': 'empathetic', 
            'excited': 'excited',
            'calm': 'calm',
            'professional': 'news'
        }
        
        voice_style = style_map.get(style, 'friendly')
        
        return f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-IN">
            <voice name="en-IN-PrabhatNeural">
                <mstts:express-as style="{voice_style}">
                    <prosody rate="0.9" pitch="+5%">
                        {text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """
    
    async def _test_speech_synthesis(self):
        """Test speech synthesis"""
        test_text = "Hello! I'm Rudh, your AI companion."
        audio_data = await self.synthesize_speech(test_text)
        if audio_data and len(audio_data) > 0:
            self.logger.info("Speech synthesis test successful")
        else:
            raise Exception("Speech synthesis test failed")

class RudhTranslator:
    """Azure Translator integration for multilingual support"""
    
    def __init__(self, credential_manager: AzureCredentialManager):
        self.credential_manager = credential_manager
        self.client = None
        self.logger = logging.getLogger('RudhTranslator')
        
    async def initialize(self, region: str) -> bool:
        """Initialize Translator service"""
        try:
            # Get Translator key from Key Vault
            translator_key = await self.credential_manager.get_secret("rudh-translator-key")
            if not translator_key:
                self.logger.error("Failed to retrieve Translator API key")
                return False
                
            # Initialize Translator client
            credential = AzureKeyCredential(translator_key)
            self.client = TextTranslationClient(
                endpoint="https://api.cognitive.microsofttranslator.com",
                credential=credential,
                region=region
            )
            
            # Test translation
            await self._test_translation()
            
            self.logger.info("Translator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Translator: {e}")
            return False
    
    async def translate_text(self, text: str, target_language: str, 
                           source_language: str = None) -> Dict:
        """Translate text with cultural context awareness"""
        try:
            if not self.client:
                raise Exception("Translator not initialized")
                
            # Prepare translation request
            input_text = [{"text": text}]
            
            # Perform translation
            response = self.client.translate(
                content=input_text,
                to=[target_language],
                from_language=source_language
            )
            
            translation_result = response[0]
            
            return {
                'translated_text': translation_result.translations[0].text,
                'detected_language': translation_result.detected_language.language if translation_result.detected_language else source_language,
                'confidence': translation_result.detected_language.score if translation_result.detected_language else 1.0,
                'target_language': target_language
            }
            
        except Exception as e:
            self.logger.error(f"Translation failed: {e}")
            raise
    
    async def _test_translation(self):
        """Test translation service"""
        test_result = await self.translate_text("Hello", "ta")  # English to Tamil
        if test_result and 'translated_text' in test_result:
            self.logger.info("Translation test successful")
        else:
            raise Exception("Translation test failed")

class RudhAzureIntegration:
    """Main Azure services integration manager for Rudh"""
    
    def __init__(self, config: AzureServiceConfig):
        self.config = config
        self.credential_manager = None
        self.openai_service = None
        self.speech_service = None
        self.translator_service = None
        self.logger = logging.getLogger('RudhAzureIntegration')
        
        # Integration status
        self.services_status = {
            'credentials': False,
            'openai': False,
            'speech': False,
            'translator': False,
            'search': False
        }
        
    async def initialize_all_services(self) -> Dict[str, bool]:
        """Initialize all Azure services for Rudh"""
        try:
            self.logger.info("Initializing Azure services for Rudh...")
            
            # Initialize credential management
            key_vault_url = f"https://{self.config.key_vault_name}.vault.azure.net/"
            self.credential_manager = AzureCredentialManager(key_vault_url)
            self.services_status['credentials'] = await self.credential_manager.initialize()
            
            if not self.services_status['credentials']:
                self.logger.error("Failed to initialize credentials. Stopping initialization.")
                return self.services_status
            
            # Initialize services concurrently for faster startup
            initialization_tasks = [
                self._initialize_openai(),
                self._initialize_speech(),
                self._initialize_translator()
            ]
            
            # Wait for all services to initialize
            results = await asyncio.gather(*initialization_tasks, return_exceptions=True)
            
            # Log initialization results
            service_names = ['openai', 'speech', 'translator']
            for i, result in enumerate(results):
                service_name = service_names[i]
                if isinstance(result, Exception):
                    self.logger.error(f"{service_name} initialization failed: {result}")
                    self.services_status[service_name] = False
                else:
                    self.services_status[service_name] = result
            
            # Log overall status
            successful_services = sum(self.services_status.values())
            total_services = len(self.services_status)
            
            self.logger.info(f"Azure services initialization complete: {successful_services}/{total_services} services active")
            
            return self.services_status
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure services: {e}")
            return self.services_status
    
    async def _initialize_openai(self) -> bool:
        """Initialize OpenAI service"""
        try:
            self.openai_service = RudhAzureOpenAI(self.credential_manager)
            return await self.openai_service.initialize(
                self.config.openai_endpoint,
                self.config.openai_deployment_name
            )
        except Exception as e:
            self.logger.error(f"OpenAI initialization failed: {e}")
            return False
    
    async def _initialize_speech(self) -> bool:
        """Initialize Speech service"""
        try:
            self.speech_service = RudhSpeechServices(self.credential_manager)
            return await self.speech_service.initialize(self.config.speech_region)
        except Exception as e:
            self.logger.error(f"Speech initialization failed: {e}")
            return False
    
    async def _initialize_translator(self) -> bool:
        """Initialize Translator service"""
        try:
            self.translator_service = RudhTranslator(self.credential_manager)
            return await self.translator_service.initialize(self.config.speech_region)
        except Exception as e:
            self.logger.error(f"Translator initialization failed: {e}")
            return False
    
    async def generate_enhanced_response(self, messages: List[Dict], 
                                       response_style: str = "empathetic",
                                       target_language: str = None) -> Dict:
        """Generate enhanced response using all available Azure services"""
        try:
            response_data = {
                'text_response': None,
                'audio_response': None,
                'translated_response': None,
                'generation_metadata': {},
                'services_used': []
            }
            
            # Generate text response with OpenAI
            if self.services_status['openai'] and self.openai_service:
                text_result = await self.openai_service.generate_response(messages)
                response_data['text_response'] = text_result['content']
                response_data['generation_metadata']['openai'] = {
                    'usage': text_result.get('usage'),
                    'model': text_result.get('model')
                }
                response_data['services_used'].append('openai')
            
            # Generate audio response if speech service available
            if (self.services_status['speech'] and self.speech_service and 
                response_data['text_response']):
                try:
                    audio_data = await self.speech_service.synthesize_speech(
                        response_data['text_response'], 
                        response_style
                    )
                    response_data['audio_response'] = audio_data
                    response_data['services_used'].append('speech')
                except Exception as e:
                    self.logger.warning(f"Speech synthesis failed: {e}")
            
            # Translate response if requested and translator available
            if (target_language and self.services_status['translator'] and 
                self.translator_service and response_data['text_response']):
                try:
                    translation_result = await self.translator_service.translate_text(
                        response_data['text_response'],
                        target_language
                    )
                    response_data['translated_response'] = translation_result
                    response_data['services_used'].append('translator')
                except Exception as e:
                    self.logger.warning(f"Translation failed: {e}")
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Enhanced response generation failed: {e}")
            raise
    
    def get_service_status(self) -> Dict:
        """Get current status of all Azure services"""
        return {
            'services_status': self.services_status,
            'total_services': len(self.services_status),
            'active_services': sum(self.services_status.values()),
            'availability_percentage': (sum(self.services_status.values()) / len(self.services_status)) * 100,
            'timestamp': datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict:
        """Perform health check on all services"""
        health_status = {}
        
        try:
            # Check OpenAI service
            if self.openai_service:
                try:
                    test_messages = [{"role": "user", "content": "Health check"}]
                    await self.openai_service.generate_response(test_messages, max_tokens=5)
                    health_status['openai'] = 'healthy'
                except Exception as e:
                    health_status['openai'] = f'unhealthy: {str(e)[:100]}'
            else:
                health_status['openai'] = 'not_initialized'
            
            # Check Speech service
            if self.speech_service:
                try:
                    await self.speech_service.synthesize_speech("Test", "friendly")
                    health_status['speech'] = 'healthy'
                except Exception as e:
                    health_status['speech'] = f'unhealthy: {str(e)[:100]}'
            else:
                health_status['speech'] = 'not_initialized'
            
            # Check Translator service
            if self.translator_service:
                try:
                    await self.translator_service.translate_text("Test", "ta")
                    health_status['translator'] = 'healthy'
                except Exception as e:
                    health_status['translator'] = f'unhealthy: {str(e)[:100]}'
            else:
                health_status['translator'] = 'not_initialized'
            
            return {
                'overall_health': 'healthy' if all('healthy' in status for status in health_status.values()) else 'degraded',
                'service_details': health_status,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'overall_health': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Configuration helper
class AzureConfigBuilder:
    """Helper to build Azure configuration from environment or Key Vault"""
    
    @staticmethod
    def from_environment() -> AzureServiceConfig:
        """Build config from environment variables"""
        import os
        
        return AzureServiceConfig(
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID', ''),
            resource_group=os.getenv('RUDH_RESOURCE_GROUP', 'rg-rudh-ai-services-sea'),
            region=os.getenv('RUDH_AZURE_REGION', 'southeastasia'),
            key_vault_name=os.getenv('RUDH_KEY_VAULT_NAME', 'kv-rudh-secrets-sea'),
            openai_endpoint=os.getenv('RUDH_OPENAI_ENDPOINT', ''),
            openai_deployment_name=os.getenv('RUDH_OPENAI_DEPLOYMENT', 'rudh-gpt4'),
            speech_key=os.getenv('RUDH_SPEECH_KEY', ''),
            speech_region=os.getenv('RUDH_SPEECH_REGION', 'southeastasia'),
            translator_key=os.getenv('RUDH_TRANSLATOR_KEY', ''),
            search_endpoint=os.getenv('RUDH_SEARCH_ENDPOINT', ''),
            search_key=os.getenv('RUDH_SEARCH_KEY', '')
        )
    
    @staticmethod
    def for_development() -> AzureServiceConfig:
        """Build config for development environment"""
        return AzureServiceConfig(
            subscription_id='dev-subscription',
            resource_group='rg-rudh-dev-sea',
            region='southeastasia',
            key_vault_name='kv-rudh-dev-sea',
            openai_endpoint='https://rudh-openai-dev.openai.azure.com/',
            openai_deployment_name='rudh-gpt4-dev',
            speech_key='dev-speech-key',
            speech_region='southeastasia',
            translator_key='dev-translator-key',
            search_endpoint='https://rudh-search-dev.search.windows.net',
            search_key='dev-search-key'
        )