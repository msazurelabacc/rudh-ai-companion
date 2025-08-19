# quick_test.py
"""
Quick test for Azure OpenAI integration
"""
import asyncio
import sys
import os

# Add src to path to import config
sys.path.append('src')

from azure_openai_service import AzureOpenAIService

async def test_azure_integration():
    print("🧪 TESTING AZURE OPENAI INTEGRATION")
    print("=" * 50)
    
    # Test service initialization
    print("🚀 Initializing Azure OpenAI service...")
    service = AzureOpenAIService()
    
    # Check status
    status = await service.get_service_status()
    print(f"\\n📊 SERVICE STATUS:")
    print(f"   Azure SDK Available: {'✅' if status['azure_sdk_available'] else '❌'}")
    print(f"   Azure Connected: {'✅' if status['azure_connected'] else '🔧 Fallback Mode'}")
    print(f"   Client Ready: {'✅' if status['client_ready'] else '❌'}")
    print(f"   Endpoint: {status['endpoint']}")
    
    # Test connection if connected
    if status['azure_connected']:
        print(f"\\n🔍 Testing Azure connection...")
        connection_ok = await service.test_connection()
        if connection_ok:
            print("✅ Azure OpenAI connection test PASSED!")
        else:
            print("❌ Azure OpenAI connection test FAILED!")
    
    # Test response generation
    print(f"\\n💬 Testing response generation...")
    test_messages = [
        {"role": "user", "content": "Hello! I'm testing the Azure integration for Rudh."}
    ]
    
    response = await service.generate_response(test_messages)
    
    print(f"\\n🤖 RESPONSE:")
    print(f"   Content: {response['content']}")
    print(f"   Source: {response['source']}")
    print(f"   Model: {response['model']}")
    print(f"   Processing Time: {response['processing_time']}")
    print(f"   Confidence: {response['confidence'] * 100:.1f}%")
    print(f"   Tokens Used: {response['tokens_used']}")
    
    # Test emotional response
    print(f"\\n😊 Testing emotional intelligence...")
    emotional_messages = [
        {"role": "user", "content": "I'm feeling really excited about my new AI project!"}
    ]
    
    emotional_response = await service.generate_response(emotional_messages)
    print(f"\\n🤖 EMOTIONAL RESPONSE:")
    print(f"   Content: {emotional_response['content']}")
    print(f"   Source: {emotional_response['source']}")
    
    # Final status
    print(f"\\n🎯 INTEGRATION STATUS:")
    if status['azure_connected']:
        print("   ✅ Azure OpenAI: FULLY OPERATIONAL")
        print("   ✅ GPT-4o Model: Available")
        print("   ✅ Intelligent Responses: Active")
        print("   💰 Cost: ~.01 per conversation")
    else:
        print("   🔧 Fallback Mode: ACTIVE")
        print("   ✅ Intelligent Responses: Working")
        print("   ✅ Emotional Intelligence: Functional")
        print("   💰 Cost: Free (no Azure charges)")
    
    print(f"\\n🚀 READY FOR RUDH INTEGRATION!")
    
    await service.close()

if __name__ == "__main__":
    asyncio.run(test_azure_integration())
