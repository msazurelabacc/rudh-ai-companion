"""
Rudh AI Interactive Interface V3 - Phase 2.2
Context-aware conversational AI with advanced emotion detection and response strategies
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Any
import json

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from rudh_core.core import EnhancedRudhCore
    from rudh_core.emotion_engine import EnhancedEmotionEngine
    from rudh_core.context_engine import AdvancedContextEngine
except ImportError as e:
    print(f"⚠️  Import Error: {e}")
    print("📁 Please ensure you have the following files in src/rudh_core/:")
    print("   - emotion_engine.py")
    print("   - context_engine.py") 
    print("   - core.py")
    sys.exit(1)

class RudhInteractiveV3:
    """
    Advanced interactive interface for Rudh AI with context awareness
    """
    
    def __init__(self):
        """Initialize the enhanced Rudh interface"""
        print("🤖 Initializing Rudh AI Companion V3...")
        print("🧠 Loading enhanced emotion detection engine...")
        print("🎯 Loading advanced context analysis engine...")
        print("⚡ Optimizing response generation strategies...")
        
        try:
            self.rudh_core = EnhancedRudhCore()
            self.session_active = True
            self.conversation_count = 0
            
            print("✅ Rudh AI Companion V3 ready!")
            
        except Exception as e:
            print(f"❌ Failed to initialize Rudh: {e}")
            sys.exit(1)
    
    def display_welcome(self):
        """Display welcome message with capabilities"""
        print("\n" + "="*80)
        print("🤖 RUDH AI COMPANION - VERSION 3.0 (Phase 2.2)")
        print("   Advanced Context-Aware Conversational AI")
        print("="*80)
        print()
        print("🌟 NEW FEATURES:")
        print("   ✅ 16+ emotion types with confidence scoring")
        print("   ✅ Advanced context analysis (7 topic categories)")
        print("   ✅ Intelligent response strategies (5 types)")
        print("   ✅ Multi-turn conversation awareness")
        print("   ✅ User personality learning")
        print("   ✅ Conversation stage detection")
        print("   ✅ Urgency and formality assessment")
        print("   ✅ Real-time performance analytics")
        print()
        print("💬 CONVERSATION CAPABILITIES:")
        print("   🎯 Context-aware responses")
        print("   😊 Emotion-sensitive communication")
        print("   🧠 Analytical problem solving")
        print("   📚 Educational explanations")
        print("   💪 Motivational support")
        print("   🤝 Empathetic conversation")
        print()
        print("📊 ANALYTICS FEATURES:")
        print("   📈 Real-time emotion tracking")
        print("   🎪 Conversation stage monitoring")
        print("   👤 User personality profiling")
        print("   ⚡ Performance metrics")
        print()
        print("Commands: '/help' - show commands, '/stats' - session stats, '/insights' - user insights")
        print("          '/summary' - conversation summary, '/reset' - new session, '/quit' - exit")
        print("-"*80)
    
    def display_help(self):
        """Display help information"""
        print("\n📖 RUDH AI COMPANION V3 - HELP")
        print("="*50)
        print()
        print("🗣️  CONVERSATION:")
        print("   • Just type naturally - Rudh understands context and emotions")
        print("   • Ask questions, share feelings, request advice")
        print("   • Rudh adapts to your communication style over time")
        print()
        print("📋 COMMANDS:")
        print("   /help     - Show this help message")
        print("   /stats    - Display detailed session statistics")
        print("   /insights - Show user personality and learning insights")
        print("   /summary  - Get conversation summary")
        print("   /reset    - Start a new session (preserves user profile)")
        print("   /quit     - Exit Rudh AI Companion")
        print()
        print("🎯 RUDH SPECIALIZES IN:")
        print("   Work & Career       - Professional advice and stress management")
        print("   Relationships       - Communication and conflict resolution")
        print("   Health & Wellness   - Emotional support and guidance")
        print("   Finance & Investment- Financial planning and advice")
        print("   Personal Growth     - Goal setting and motivation")
        print("   Technology & Learning- Education and skill development")
        print("   Creative Projects   - Artistic and creative guidance")
        print()
        print("🔮 ADVANCED FEATURES:")
        print("   • Emotion Recognition: 16+ emotions with confidence levels")
        print("   • Context Awareness: Understands conversation flow and topics")
        print("   • Response Strategies: Adapts communication style")
        print("   • Learning Memory: Builds understanding of your preferences")
        print("   • Performance Analytics: Real-time processing metrics")
        print()
    
    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return enhanced response"""
        self.conversation_count += 1
        
        # Display processing indicator
        print("🧠 Analyzing...", end="", flush=True)
        
        # Process with enhanced core
        result = await self.rudh_core.process_message(user_input)
        
        # Clear processing indicator
        print("\r" + " "*15 + "\r", end="", flush=True)
        
        return result
    
    def display_response(self, result: Dict[str, Any]):
        """Display the AI response with enhanced analytics"""
        # Main response
        print(f"🤖 Rudh: {result['response']}")
        
        # Enhanced analytics (compact format)
        emotion = result['emotion_analysis']
        context = result['context_analysis']
        strategy = result['response_strategy']
        performance = result['performance_metrics']
        
        print(f"\n📊 Analysis: {emotion['primary_emotion'].title()} ({emotion['confidence']:.0%}) | "
              f"Topic: {context['topic'].title()} | "
              f"Strategy: {strategy['strategy_type'].title()} ({strategy['confidence']:.0%}) | "
              f"Stage: {context['conversation_stage'].title()} | "
              f"Time: {performance['total_processing_time']}")
        
        # Show follow-up suggestions if available
        if strategy.get('follow_up_suggestions'):
            print(f"💡 Suggestion: {strategy['follow_up_suggestions'][0]}")
    
    def display_detailed_analytics(self, result: Dict[str, Any]):
        """Display detailed analytics for the response"""
        print("\n" + "="*60)
        print("📊 DETAILED ANALYSIS")
        print("="*60)
        
        # Emotion Analysis
        emotion = result['emotion_analysis']
        print(f"\n😊 EMOTION ANALYSIS:")
        print(f"   Primary Emotion: {emotion['primary_emotion'].title()} ({emotion['confidence']:.1%} confidence)")
        print(f"   Intensity Level: {emotion['intensity'].title()}")
        if emotion.get('secondary_emotions'):
            print(f"   Secondary Emotions: {', '.join(emotion['secondary_emotions'])}")
        print(f"   Processing Time: {emotion['processing_time']}")
        
        # Context Analysis
        context = result['context_analysis']
        print(f"\n🎯 CONTEXT ANALYSIS:")
        print(f"   Primary Topic: {context['topic'].title()}")
        print(f"   Conversation Stage: {context['conversation_stage'].title()}")
        print(f"   User Goals: {', '.join(context['user_goals'])}")
        print(f"   Urgency Level: {context['urgency_level'].title()}")
        print(f"   Formality Level: {context['formality_level'].title()}")
        if context.get('key_entities'):
            print(f"   Key Entities: {', '.join(context['key_entities'])}")
        if context.get('mood_trend'):
            print(f"   Recent Mood Trend: {' → '.join(context['mood_trend'][-3:])}")
        print(f"   Processing Time: {context['processing_time']}")
        
        # Response Strategy
        strategy = result['response_strategy']
        print(f"\n🧠 RESPONSE STRATEGY:")
        print(f"   Strategy Type: {strategy['strategy_type'].title()} ({strategy['confidence']:.1%} confidence)")
        print(f"   Reasoning: {strategy['reasoning']}")
        print(f"   Content Focus: {', '.join(strategy['content_focus'])}")
        if strategy.get('follow_up_suggestions'):
            print(f"   Follow-up Suggestions:")
            for i, suggestion in enumerate(strategy['follow_up_suggestions'], 1):
                print(f"     {i}. {suggestion}")
        print(f"   Processing Time: {strategy['processing_time']}")
        
        # Performance Metrics
        performance = result['performance_metrics']
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"   Total Processing: {performance['total_processing_time']}")
        print(f"   Emotion Analysis: {performance['emotion_processing']}")
        print(f"   Context Analysis: {performance['context_processing']}")
        print(f"   Strategy Selection: {performance['strategy_processing']}")
        print(f"   Response Generation: {performance['response_generation']}")
        print(f"   Memory Update: {performance['memory_update']}")
        
        # Session Information
        session = result['session_info']
        print(f"\n📈 SESSION INFO:")
        print(f"   Message Count: {session['message_count']}")
        print(f"   Session Duration: {session['session_duration']}")
        print(f"   Average Confidence: {session['average_confidence']}")
        
        print("="*60)
    
    def display_session_stats(self):
        """Display comprehensive session statistics"""
        try:
            summary = self.rudh_core.get_conversation_summary()
            
            print("\n" + "="*60)
            print("📊 SESSION STATISTICS")
            print("="*60)
            
            print(f"\n💬 CONVERSATION OVERVIEW:")
            print(f"   Total Messages: {summary.get('message_count', 0)}")
            print(f"   Session Duration: {summary.get('session_duration', 'Unknown')}")
            print(f"   Current Stage: {summary.get('conversation_stage', 'Unknown').title()}")
            print(f"   Average Confidence: {summary.get('average_confidence', 'N/A')}")
            
            print(f"\n🎭 EMOTION & TOPIC PATTERNS:")
            print(f"   Recent Topics: {', '.join(summary.get('recent_topics', ['None']))}")
            print(f"   Recent Emotions: {', '.join(summary.get('recent_emotions', ['None']))}")
            print(f"   Most Discussed Topic: {summary.get('most_discussed_topic', 'None').title()}")
            print(f"   Most Common Emotion: {summary.get('most_common_emotion', 'None').title()}")
            
            # Get additional analytics from core
            if hasattr(self.rudh_core, 'session_stats'):
                stats = self.rudh_core.session_stats
                
                print(f"\n📈 PROCESSING PERFORMANCE:")
                avg_time = stats['total_processing_time'] / max(stats['messages_processed'], 1)
                print(f"   Average Response Time: {avg_time:.3f}s")
                print(f"   Total Processing Time: {stats['total_processing_time']:.3f}s")
                
                if stats['emotions_detected']:
                    print(f"\n😊 EMOTION DISTRIBUTION:")
                    for emotion, count in sorted(stats['emotions_detected'].items(), key=lambda x: x[1], reverse=True):
                        percentage = (count / stats['messages_processed']) * 100
                        print(f"   {emotion.title()}: {count} times ({percentage:.1f}%)")
                
                if stats['topics_discussed']:
                    print(f"\n🎯 TOPIC DISTRIBUTION:")
                    for topic, count in sorted(stats['topics_discussed'].items(), key=lambda x: x[1], reverse=True):
                        percentage = (count / stats['messages_processed']) * 100
                        print(f"   {topic.title()}: {count} times ({percentage:.1f}%)")
                
                if stats['strategies_used']:
                    print(f"\n🧠 STRATEGY USAGE:")
                    for strategy, count in sorted(stats['strategies_used'].items(), key=lambda x: x[1], reverse=True):
                        percentage = (count / stats['messages_processed']) * 100
                        print(f"   {strategy.title()}: {count} times ({percentage:.1f}%)")
            
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error displaying session stats: {e}")
    
    def display_user_insights(self):
        """Display user personality and learning insights"""
        try:
            insights = self.rudh_core.get_user_insights()
            
            print("\n" + "="*60)
            print("👤 USER INSIGHTS & PERSONALITY PROFILE")
            print("="*60)
            
            # Personality Profile
            personality = insights['personality_profile']
            print(f"\n🧠 PERSONALITY ANALYSIS:")
            print(f"   Dominant Trait: {personality['dominant_trait']}")
            print(f"   Analytical Tendency: {personality['analytical_tendency']}")
            print(f"   Emotional Tendency: {personality['emotional_tendency']}")
            print(f"   Creative Tendency: {personality['creative_tendency']}")
            
            # Communication Style
            comm_style = insights['communication_style']
            print(f"\n💬 COMMUNICATION PREFERENCES:")
            print(f"   Detail Level: {comm_style['preferred_detail_level']}")
            print(f"   Formality Preference: {comm_style['formality_preference']}")
            print(f"   Directness Style: {comm_style['directness_preference']}")
            
            # Interests and Patterns
            interests = insights['interests_and_patterns']
            print(f"\n🎯 INTERESTS & LEARNING PATTERNS:")
            print(f"   Top Discussion Topics: {', '.join(interests['top_topics']) if interests['top_topics'] else 'Still learning...'}")
            print(f"   Profile Maturity: {interests['profile_maturity']}")
            
            learning_style = interests.get('learning_style', {})
            if learning_style:
                print(f"\n📚 LEARNING STYLE PREFERENCES:")
                for key, value in learning_style.items():
                    formatted_key = key.replace('_', ' ').title()
                    print(f"   {formatted_key}: {'Yes' if value else 'No'}")
            
            print("\n💡 PERSONALIZATION TIPS:")
            
            # Generate personalized tips based on insights
            dominant_trait = personality['dominant_trait'].split()[0].lower()
            detail_pref = comm_style['preferred_detail_level'].lower()
            formality_pref = comm_style['formality_preference'].lower()
            
            if dominant_trait == 'analytical':
                print("   • Rudh will provide structured, logical responses with clear reasoning")
            elif dominant_trait == 'emotional':
                print("   • Rudh will emphasize empathy and emotional support in responses")
            elif dominant_trait == 'creative':
                print("   • Rudh will offer innovative solutions and creative perspectives")
            
            if detail_pref == 'high':
                print("   • Responses will include comprehensive details and explanations")
            elif detail_pref == 'low':
                print("   • Responses will be concise and to-the-point")
            
            if formality_pref == 'formal':
                print("   • Communication will maintain professional, formal tone")
            elif formality_pref == 'casual':
                print("   • Communication will be friendly and conversational")
            
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error displaying user insights: {e}")
    
    def display_conversation_summary(self):
        """Display conversation summary"""
        try:
            summary = self.rudh_core.get_conversation_summary()
            
            print("\n" + "="*60)
            print("📝 CONVERSATION SUMMARY")
            print("="*60)
            
            print(f"\n📊 OVERVIEW:")
            print(f"   Messages Exchanged: {summary.get('message_count', 0)}")
            print(f"   Session Duration: {summary.get('session_duration', 'Unknown')}")
            print(f"   Current Conversation Stage: {summary.get('conversation_stage', 'Unknown').title()}")
            
            print(f"\n🎭 EMOTIONAL JOURNEY:")
            recent_emotions = summary.get('recent_emotions', [])
            if recent_emotions:
                print(f"   Emotional Progression: {' → '.join([e.title() for e in recent_emotions])}")
            else:
                print("   Emotional Progression: Not enough data")
            
            print(f"\n🎯 TOPICS COVERED:")
            recent_topics = summary.get('recent_topics', [])
            if recent_topics:
                for i, topic in enumerate(recent_topics, 1):
                    print(f"   {i}. {topic.title()}")
            else:
                print("   No specific topics identified yet")
            
            print(f"\n📈 ENGAGEMENT METRICS:")
            print(f"   Average Confidence: {summary.get('average_confidence', 'N/A')}")
            print(f"   Most Discussed Topic: {summary.get('most_discussed_topic', 'None').title()}")
            print(f"   Predominant Emotion: {summary.get('most_common_emotion', 'None').title()}")
            
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error displaying conversation summary: {e}")
    
    def reset_session(self):
        """Reset the session while preserving user profile"""
        try:
            self.rudh_core.reset_session()
            self.conversation_count = 0
            print("\n🔄 Session Reset Successfully!")
            print("✅ User profile and preferences preserved")
            print("🆕 New conversation session started")
            print("-"*50)
        except Exception as e:
            print(f"❌ Error resetting session: {e}")
    
    async def main_loop(self):
        """Main interactive loop"""
        self.display_welcome()
        
        while self.session_active:
            try:
                # Get user input
                print(f"\n[{self.conversation_count + 1}] ", end="")
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command = user_input.lower()
                    
                    if command == '/quit' or command == '/exit':
                        print("\n👋 Thank you for using Rudh AI Companion V3!")
                        print("🌟 Your conversation data and preferences have been saved.")
                        print("💭 Remember: I'm always here when you need thoughtful, context-aware assistance.")
                        self.session_active = False
                        break
                    
                    elif command == '/help':
                        self.display_help()
                    
                    elif command == '/stats':
                        self.display_session_stats()
                    
                    elif command == '/insights':
                        self.display_user_insights()
                    
                    elif command == '/summary':
                        self.display_conversation_summary()
                    
                    elif command == '/reset':
                        self.reset_session()
                    
                    elif command == '/debug':
                        # Hidden command for detailed analytics on last response
                        if hasattr(self, 'last_result'):
                            self.display_detailed_analytics(self.last_result)
                        else:
                            print("⚠️ No recent response to analyze")
                    
                    else:
                        print(f"❓ Unknown command: {user_input}")
                        print("💡 Type '/help' to see available commands")
                    
                    continue
                
                # Process regular conversation
                result = await self.process_user_input(user_input)
                self.last_result = result  # Store for debug command
                
                # Display response
                self.display_response(result)
                
                # Optional: Show detailed analytics for interesting responses
                if (result['emotion_analysis']['confidence'] > 0.8 or 
                    result['response_strategy']['confidence'] > 0.8):
                    print("💡 Type '/debug' to see detailed analysis of this response")
                
            except KeyboardInterrupt:
                print("\n\n⏸️  Conversation paused.")
                print("💬 Type '/quit' to exit or continue the conversation...")
                continue
            
            except Exception as e:
                print(f"\n❌ Error during conversation: {e}")
                print("🔄 Please try again or type '/help' for assistance")
                continue

def main():
    """Main entry point"""
    try:
        # Initialize and run Rudh Interactive V3
        rudh_interface = RudhInteractiveV3()
        
        # Run the main interactive loop
        asyncio.run(rudh_interface.main_loop())
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using Rudh AI Companion V3!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("🔧 Please check your installation and try again")

if __name__ == "__main__":
    main()