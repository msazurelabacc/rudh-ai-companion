"""
Emoji-free version of Rudh interactive for testing
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rudh_core.core import RudhCore
from config.config import RudhConfig

async def start_rudh_clean():
    """Start Rudh in interactive mode without emoji logging issues"""
    print("Welcome to Rudh AI Companion!")
    print("Built in Chennai, India")
    print("Powered by Azure AI")
    print("="*50)
    
    # Initialize Rudh
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    print("Initializing Rudh...")
    success = await rudh.initialize()
    
    if not success:
        print("Rudh started with limited functionality")
    
    print("\nYou can now chat with Rudh! (Type 'quit' to exit)")
    print("-" * 50)
    
    # Interactive chat loop
    while True:
        try:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! Rudh is going to sleep...")
                break
            
            if user_input.strip() == "":
                continue
            
            print("Rudh is thinking...")
            response = await rudh.process_message(user_input, "interactive_user")
            
            print(f"Rudh: {response['response']}")
            
            # Show debug info
            emotion = response['emotion_detected']['primary_emotion']
            strategy = response.get('strategy_used', 'unknown')
            language = response.get('language_detected', 'unknown')
            print(f"[Debug: Emotion={emotion}, Strategy={strategy}, Language={language}]")
            
        except KeyboardInterrupt:
            print("\nGoodbye! Rudh is going to sleep...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting Rudh AI Companion - Clean Version!")
    asyncio.run(start_rudh_clean())
