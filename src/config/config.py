"""
Configuration management for Rudh AI Companion
Enhanced with multi-region Azure services
"""
import os
from typing import Dict, Optional

class RudhConfig:
    """Configuration management for Rudh"""
    
    @staticmethod
    def get_config(environment: str = "development") -> Dict:
        """Get configuration based on environment"""
        
        base_config = {
            "azure": {
                # Multi-region setup: OpenAI in East US 2, Speech in Southeast Asia
                "regions": {
                    "primary": "southeastasia",
                    "ai_models": "eastus2"
                },
                
                # OpenAI Configuration (East US 2)
                "openai": {
                    "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "https://oai-rudh-core-dev-eus2.openai.azure.com/"),
                    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                    "api_version": "2024-05-01-preview",
                    "region": "eastus2",
                    "deployments": {
                        "gpt4o": os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4O", "rudh-gpt4o"),
                        "gpt4": os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4", "rudh-gpt4"),
                        "primary_model": "gpt4o"
                    }
                },
                
                # Speech Services Configuration (Southeast Asia)
                "speech": {
                    "key": os.getenv("AZURE_SPEECH_KEY"),
                    "region": os.getenv("AZURE_SPEECH_REGION", "southeastasia"),
                    "endpoint": "https://southeastasia.api.cognitive.microsoft.com/",
                    "voice": os.getenv("AZURE_SPEECH_VOICE", "en-IN-NeerjaNeural"),
                    "rate": "medium",
                    "pitch": "medium",
                    "style": "friendly"
                },
                
                # Translator Configuration (Southeast Asia)
                "translator": {
                    "key": os.getenv("AZURE_TRANSLATOR_KEY"),
                    "region": "southeastasia",
                    "endpoint": "https://api.cognitive.microsofttranslator.com/"
                },
                
                # Key Vault Configuration
                "key_vault": {
                    "name": os.getenv("AZURE_KEYVAULT_NAME", "kv-rudh-secrets-sea"),
                    "url": os.getenv("AZURE_KEYVAULT_URL", "https://kv-rudh-secrets-sea.vault.azure.net/"),
                    "region": "southeastasia"
                }
            },
            
            "rudh": {
                "name": "Rudh",
                "version": "2.3.0",  # Updated to reflect Phase 2.3
                "personality": "empathetic_intelligent_companion",
                "primary_languages": ["tamil", "english"],
                "response_style": "warm_professional",
                "memory_limit": 50,
                "max_response_tokens": 500,
                "temperature": 0.7,
                
                # Enhanced capabilities
                "features": {
                    "azure_openai": True,
                    "speech_synthesis": True,
                    "real_time_translation": True,
                    "emotional_intelligence": True,
                    "context_awareness": True,
                    "user_profiling": True
                }
            },
            
            "development": {
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
                "debug_mode": os.getenv("DEBUG_MODE", "true").lower() == "true",
                "test_mode": False,
                "mock_responses": os.getenv("MOCK_RESPONSES", "true").lower() == "true",
                "azure_fallback": True  # Enable graceful fallback when Azure unavailable
            },
            
            "api": {
                "host": "0.0.0.0",
                "port": int(os.getenv("PORT", "8000")),
                "reload": True,
                "cors_origins": ["*"],  # Restrict in production
                "rate_limit": {
                    "requests_per_minute": 60,
                    "burst_limit": 10
                }
            },
            
            # Performance and monitoring
            "performance": {
                "response_timeout": 30,
                "max_retries": 3,
                "health_check_interval": 300,  # 5 minutes
                "metrics_enabled": True
            }
        }
        
        # Environment-specific overrides
        if environment == "production":
            base_config["development"]["debug_mode"] = False
            base_config["development"]["test_mode"] = False
            base_config["development"]["mock_responses"] = False
            base_config["api"]["reload"] = False
            base_config["api"]["cors_origins"] = ["https://yourdomain.com"]
            base_config["development"]["log_level"] = "WARNING"
        
        return base_config
    
    @staticmethod
    def get_azure_credentials() -> Dict:
        """Get Azure credentials from environment or Key Vault"""
        return {
            "openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "speech_key": os.getenv("AZURE_SPEECH_KEY"),
            "translator_key": os.getenv("AZURE_TRANSLATOR_KEY"),
            "keyvault_url": os.getenv("AZURE_KEYVAULT_URL")
        }
    
    @staticmethod
    def get_openai_config() -> Dict:
        """Get OpenAI specific configuration"""
        config = RudhConfig.get_config()
        return config["azure"]["openai"]
    
    @staticmethod
    def get_speech_config() -> Dict:
        """Get Speech Services configuration"""
        config = RudhConfig.get_config()
        return config["azure"]["speech"]
    
    @staticmethod
    def get_keyvault_config() -> Dict:
        """Get Key Vault configuration"""
        config = RudhConfig.get_config()
        return config["azure"]["key_vault"]
    
    @staticmethod
    def validate_config(config: Dict) -> bool:
        """Validate configuration completeness"""
        required_keys = ["azure", "rudh", "development"]
        
        for key in required_keys:
            if key not in config:
                return False
        
        # Validate Azure configuration
        azure_config = config.get("azure", {})
        required_azure_keys = ["openai", "speech", "key_vault"]
        
        for key in required_azure_keys:
            if key not in azure_config:
                return False
        
        return True
    
    @staticmethod
    def get_azure_status() -> Dict:
        """Get Azure services availability status"""
        credentials = RudhConfig.get_azure_credentials()
        
        return {
            "openai_configured": bool(credentials.get("openai_endpoint") and credentials.get("openai_api_key")),
            "speech_configured": bool(credentials.get("speech_key")),
            "translator_configured": bool(credentials.get("translator_key")),
            "keyvault_configured": bool(credentials.get("keyvault_url")),
            "multi_region_setup": True
        }

# Backward compatibility
def get_config(environment: str = "development") -> Dict:
    """Backward compatible function"""
    return RudhConfig.get_config(environment)