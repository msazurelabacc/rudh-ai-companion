"""
Clean Rudh Interactive - No emoji logging issues
Enhanced with proper strategy detection and responses
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rudh_core.core import RudhCore
from config.config import RudhConfig

async def start_rudh_enhanced():
    """Start Rudh in interactive mode with enhanced capabilities"""
    print("=" * 60)
    print("           RUDH AI COMPANION - ENHANCED VERSION")
    print("=" * 60)
    print("Built in Chennai, India | Powered by Azure AI")
    print("Your intelligent companion for life, finance, and creativity")
    print("=" * 60)
    
    # Initialize Rudh
    config = RudhConfig.get_config()
    rudh = RudhCore(config)
    
    print("\n[SYSTEM] Initializing Rudh AI Core...")
    success = await rudh.initialize()
    
    if not success:
        print("[WARNING] Rudh started with limited functionality")
    else:
        print("[SUCCESS] Rudh AI Core fully initialized!")
    
    print("\n" + "=" * 60)
    print("CONVERSATION STARTED - Type 'quit', 'exit', or 'bye' to end")
    print("=" * 60)
    
    # Test different capabilities
    print("\nTry these examples:")
    print("• General: 'Hello Rudh, how are you?'")
    print("• Tamil: 'வணக்கம் ருத்!'")
    print("• Financial: 'Give me investment advice'")
    print("• Emotional: 'I'm feeling stressed today'")
    print("• Creative: 'Help me create a business plan'")
    print("• Knowledge: 'Explain artificial intelligence'")
    print("-" * 60)
    
    conversation_count = 0
    
    # Interactive chat loop
    while True:
        try:
            user_input = input(f"\n[{conversation_count + 1}] You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n[SYSTEM] Goodbye! Rudh is going to sleep...")
                print("Thank you for chatting with Rudh!")
                break
            
            if user_input.strip() == "":
                print("[SYSTEM] Please enter a message.")
                continue
            
            # Special commands
            if user_input.lower() == 'stats':
                stats = rudh.get_stats()
                print("\n[RUDH STATS]")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                continue
            
            if user_input.lower() == 'history':
                history = rudh.get_conversation_history(limit=5)
                print(f"\n[CONVERSATION HISTORY] Last {len(history)} messages:")
                for i, conv in enumerate(history, 1):
                    print(f"  {i}. User: {conv['user_input'][:50]}...")
                    print(f"     Rudh: {conv['rudh_response'][:50]}...")
                continue
            
            print(f"[SYSTEM] Rudh is thinking... (Processing message {conversation_count + 1})")
            response = await rudh.process_message(user_input, "interactive_user")
            
            # Display response
            print(f"\n[RUDH]: {response['response']}")
            
            # Display analysis details
            emotion = response['emotion_detected']['primary_emotion']
            strategy = response.get('strategy_used', 'unknown')
            language = response.get('language_detected', 'unknown')
            confidence = response.get('confidence', 0.0)
            
            print(f"\n[ANALYSIS]")
            print(f"  Emotion: {emotion.title()}")
            print(f"  Strategy: {strategy.replace('_', ' ').title()}")
            print(f"  Language: {language.title()}")
            print(f"  Confidence: {confidence:.1%}")
            
            conversation_count += 1
            
            # Show additional emotions if detected
            all_emotions = response['emotion_detected'].get('all_emotions', [])
            if len(all_emotions) > 1:
                other_emotions = [e for e in all_emotions if e != emotion]
                print(f"  Also detected: {', '.join(other_emotions)}")
            
        except KeyboardInterrupt:
            print("\n\n[SYSTEM] Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] Something went wrong: {e}")
            print("[SYSTEM] Let's try again...")

    # Final statistics
    print(f"\n[SESSION SUMMARY]")
    print(f"  Total conversations: {conversation_count}")
    print(f"  Rudh memory size: {len(rudh.conversation_memory)}")
    print(f"  Session status: Completed successfully")
    print("\n" + "=" * 60)
    print("Thank you for using Rudh AI Companion!")
    print("=" * 60)

if __name__ == "__main__":
    print("Starting Rudh AI Companion - Enhanced Clean Version!")
    asyncio.run(start_rudh_enhanced())