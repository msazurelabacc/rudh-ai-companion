"""
Basic tests for Rudh Core functionality
"""
import pytest
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rudh_core.core import RudhCore
from config.config import RudhConfig

@pytest.mark.asyncio
async def test_rudh_initialization():
    """Test that Rudh core initializes properly"""
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    # Test basic initialization
    assert rudh.config is not None
    assert rudh.conversation_memory == []
    assert rudh.emotional_state == "neutral"
    assert rudh.is_initialized == False

@pytest.mark.asyncio  
async def test_message_processing():
    """Test basic message processing"""
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    # Test message processing
    response = await rudh.process_message("Hello Rudh, how are you?", "test_user")
    
    assert "response" in response
    assert "emotion_detected" in response
    assert "timestamp" in response
    assert len(rudh.conversation_memory) == 1

@pytest.mark.asyncio
async def test_tamil_greeting():
    """Test Tamil language support"""
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    response = await rudh.process_message("வணக்கம் ருத்!", "tamil_user")
    
    assert "response" in response
    assert "வணக்கம்" in response["response"] or "Hello" in response["response"]
    assert response["language_detected"] == "tamil"

@pytest.mark.asyncio
async def test_emotional_detection():
    """Test emotion detection"""
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    # Test sad emotion
    response = await rudh.process_message("I'm feeling really sad today", "emotional_user")
    assert response["emotion_detected"]["primary_emotion"] == "sad"
    
    # Test happy emotion
    response = await rudh.process_message("I'm so happy and excited!", "emotional_user")
    assert response["emotion_detected"]["primary_emotion"] in ["happy", "excited"]

def test_config_validation():
    """Test configuration validation"""
    config = RudhConfig.get_config()
    assert RudhConfig.validate_config(config) == True

if __name__ == "__main__":
    # Quick interactive test
    async def quick_test():
        print("🧪 Testing Rudh Core...")
        
        config = RudhConfig.get_config()
        rudh = RudhCore(config)
        
        # Test basic conversation
        test_messages = [
            "Hello Rudh!",
            "How are you today?",
            "வணக்கம்! எப்படி இருக்கீங்க?",
            "I'm feeling a bit sad today",
            "Can you help me with investment advice?",
            "Thank you so much!"
        ]
        
        print("\n" + "="*50)
        print("🤖 RUDH AI COMPANION - INTERACTIVE TEST")
        print("="*50)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n[Test {i}] User: {message}")
            response = await rudh.process_message(message, f"test_user_{i}")
            print(f"[Test {i}] Rudh: {response['response']}")
            print(f"[Test {i}] Emotion: {response['emotion_detected']['primary_emotion']}")
            print(f"[Test {i}] Strategy: {response.get('strategy_used', 'unknown')}")
        
        print(f"\n📊 Final Stats:")
        stats = rudh.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n✅ Quick test completed!")
    
    # Run the test
    asyncio.run(quick_test())
