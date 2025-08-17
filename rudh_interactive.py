"""
Quick startup script for Rudh AI Companion
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rudh_core.core import RudhCore
from config.config import RudhConfig

async def start_rudh_interactive():
    """Start Rudh in interactive mode"""
    print("🤖 Starting Rudh AI Companion...")
    print("="*50)
    
    # Initialize Rudh
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    print("🧠 Initializing Rudh...")
    success = await rudh.initialize()
    
    if not success:
        print("⚠️ Rudh started with limited functionality")
    
    print("\n💬 You can now chat with Rudh! (Type 'quit' to exit)")
    print("-" * 50)
    
    # Interactive chat loop
    while True:
        try:
            user_input = input("\n👤 You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Rudh is going to sleep...")
                break
            
            if user_input.strip() == "":
                continue
            
            print("🤔 Rudh is thinking...")
            response = await rudh.process_message(user_input, "interactive_user")
            
            print(f"🤖 Rudh: {response['response']}")
            
            # Show additional info for debugging
            if config["development"]["debug_mode"]:
                print(f"   [Emotion: {response['emotion_detected']['primary_emotion']}, " +
                      f"Strategy: {response.get('strategy_used', 'unknown')}, " +
                      f"Language: {response.get('language_detected', 'unknown')}]")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Rudh is going to sleep...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🌟 Welcome to Rudh AI Companion!")
    print("🇮🇳 Built in Chennai, India")
    print("🧠 Powered by Azure AI")
    
    asyncio.run(start_rudh_interactive())
