# azure_openai_service.py
"""
Azure OpenAI Integration for Rudh - Enhanced with existing config
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import your existing config
import sys
sys.path.append('src')
from config.config import RudhConfig

try:
    from openai import AsyncAzureOpenAI
    from azure.identity import DefaultAzureCredential
    from dotenv import load_dotenv
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    print("Azure SDK not available. Install with: pip install openai azure-identity python-dotenv")

class AzureOpenAIService:
    """Azure OpenAI service using Rudh's existing configuration"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.config = RudhConfig.get_config()
        self.azure_config = self.config['azure']['openai']
        self.client = None
        self.is_available = AZURE_AVAILABLE
        self.azure_connected = False
        self.logger = logging.getLogger("AzureOpenAIService")
        
        if self.is_available:
            # Initialize synchronously for immediate use
            try:
                self._sync_initialize()
            except Exception as e:
                self.logger.error(f"Sync initialization failed: {e}")
    
    def _sync_initialize(self):
        """Synchronous initialization"""
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        
        if not endpoint or not api_key:
            self.logger.warning("Azure OpenAI credentials not found in environment")
            return
        
        # Initialize OpenAI client
        self.client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=self.azure_config['api_version']
        )
        
        self.azure_connected = True
        self.logger.info("✅ Azure OpenAI client initialized")
    
    async def test_connection(self) -> bool:
        """Test Azure OpenAI connection"""
        try:
            if not self.client:
                return False
            
            deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_GPT4O', 'rudh-gpt4o')
            
            response = await self.client.chat.completions.create(
                model=deployment,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            
            success = response.choices and len(response.choices) > 0
            if success:
                self.logger.info("✅ Azure OpenAI connection test successful")
            return success
            
        except Exception as e:
            self.logger.error(f"Azure OpenAI connection test failed: {e}")
            return False
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate response using Azure OpenAI"""
        start_time = datetime.now()
        
        try:
            if not self.client:
                return self._fallback_response(messages, start_time)
            
            deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_GPT4O', 'rudh-gpt4o')
            
            response = await self.client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', 500),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "content": response.choices[0].message.content,
                "model": deployment,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "processing_time": f"{processing_time:.3f}s",
                "source": "azure_openai",
                "confidence": 0.95,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Azure OpenAI generation failed: {e}")
            return self._fallback_response(messages, start_time)
    
    def _fallback_response(self, messages: List[Dict[str, str]], start_time: datetime) -> Dict[str, Any]:
        """Fallback response when Azure unavailable"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Get user message for context
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "").lower()
                break
        
        # Smart fallback responses
        if any(word in user_message for word in ['hello', 'hi', 'hey']):
            content = "Hello! I'm Rudh, your AI companion. I'm here to help and chat with you. How are you feeling today?"
        elif any(word in user_message for word in ['frustrated', 'angry', 'annoyed']):
            content = "I can sense your frustration, and that's completely understandable. Sometimes challenges can feel overwhelming. I'm here to listen and help you work through whatever is bothering you."
        elif any(word in user_message for word in ['excited', 'happy', 'great']):
            content = "That's wonderful to hear! Your positive energy is contagious. I'd love to hear more about what's making you feel so good today."
        else:
            content = "I'm here to help you. Could you tell me more about what's on your mind today?"
        
        return {
            "content": content,
            "model": "rudh_intelligent_fallback",
            "tokens_used": len(content.split()),
            "processing_time": f"{processing_time:.3f}s",
            "source": "intelligent_fallback",
            "confidence": 0.75,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "azure_sdk_available": self.is_available,
            "azure_connected": self.azure_connected,
            "client_ready": self.client is not None,
            "config_loaded": bool(self.config),
            "endpoint": os.getenv('AZURE_OPENAI_ENDPOINT', 'not_configured'),
            "fallback_mode": not self.azure_connected,
            "last_check": datetime.now().isoformat()
        }
    
    async def close(self):
        """Clean up resources"""
        if self.client:
            await self.client.close()
