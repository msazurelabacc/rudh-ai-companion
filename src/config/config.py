"""
Configuration management for Rudh AI Companion
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
                "openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "openai_model": os.getenv("AZURE_OPENAI_MODEL", "gpt-4"),
                "speech_key": os.getenv("AZURE_SPEECH_KEY"),
                "speech_region": os.getenv("AZURE_SPEECH_REGION", "southeastasia"),
                "translator_key": os.getenv("AZURE_TRANSLATOR_KEY"),
                "region": "southeastasia"
            },
            "rudh": {
                "name": "Rudh",
                "version": "0.1.0",
                "personality": "empathetic_intelligent_companion",
                "primary_languages": ["tamil", "english"],
                "response_style": "warm_professional",
                "memory_limit": 50,
                "max_response_tokens": 500,
                "temperature": 0.7
            },
            "development": {
                "log_level": "INFO",
                "debug_mode": True,
                "test_mode": False,
                "mock_responses": True  # Set to False when Azure services are configured
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "reload": True,
                "cors_origins": ["*"]  # Restrict in production
            }
        }
        
        # Environment-specific overrides
        if environment == "production":
            base_config["development"]["debug_mode"] = False
            base_config["development"]["test_mode"] = False
            base_config["development"]["mock_responses"] = False
            base_config["api"]["reload"] = False
            base_config["api"]["cors_origins"] = ["https://yourdomain.com"]
        
        return base_config
    
    @staticmethod
    def get_azure_credentials() -> Dict:
        """Get Azure credentials from environment or Key Vault"""
        return {
            "openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "speech_key": os.getenv("AZURE_SPEECH_KEY"),
            "translator_key": os.getenv("AZURE_TRANSLATOR_KEY")
        }
    
    @staticmethod
    def validate_config(config: Dict) -> bool:
        """Validate configuration completeness"""
        required_keys = ["azure", "rudh", "development"]
        
        for key in required_keys:
            if key not in config:
                return False
        
        return True
