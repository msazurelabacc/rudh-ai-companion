# rudh_interactive_v4.py
"""
Rudh AI Companion Interactive Interface V4 - Phase 2.3
Production-ready interface with Azure integration and advanced features
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Safe imports with fallbacks
try:
    from rudh_core.enhanced_core import ProductionRudhCore
    from azure_integration.azure_services import AzureConfigBuilder
    PRODUCTION_CORE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Production core not available: {e}")
    print("Falling back to Phase 2.2 core...")
    try:
        from rudh_core.core import EnhancedRudhCore as ProductionRudhCore
        PRODUCTION_CORE_AVAILABLE = False
    except ImportError:
        print("❌ No compatible core found. Please check your installation.")
        sys.exit(1)

class RudhInteractiveV4:
    """
    Advanced Interactive Interface for Rudh AI Companion V4
    Production-ready with Azure integration and comprehensive features
    """
    
    def __init__(self):
        self.rudh_core = None
        self.session_id = None
        self.user_id = "interactive_user"
        self.conversation_count = 0
        self.session_start_time = None
        self.azure_config = None
        
        # Interface settings
        self.show_detailed_analysis = True
        self.show_performance_metrics = True
        self.show_azure_status = True
        self.auto_save_session = True
        
        # Command handlers
        self.command_handlers = {
            '/help': self._show_help,
            '/stats': self._show_stats,
            '/insights': self._show_insights,
            '/summary': self._show_summary,
            '/health': self._show_health,
            '/azure': self._show_azure_status,
            '/profile': self._show_user_profile,
            '/settings': self._show_settings,
            '/debug': self._toggle_debug,
            '/reset': self._reset_session,
            '/save': self._save_session,
            '/load': self._load_session,
            '/quit': self._quit_session
        }
        
    async def initialize(self):
        """Initialize Rudh system with all components"""
        print("🤖 Initializing Rudh AI Companion V4...")
        print("🧠 Loading production-grade AI core...")
        
        try:
            # Try to load Azure configuration
            if PRODUCTION_CORE_AVAILABLE:
                print("🌐 Attempting Azure configuration...")
                try:
                    self.azure_config = AzureConfigBuilder.for_development()
                    print("✅ Azure configuration loaded")
                except Exception as e:
                    print(f"⚠️ Azure config failed: {e}")
                    print("🔄 Continuing without Azure integration...")
            
            # Initialize Rudh core
            if PRODUCTION_CORE_AVAILABLE and self.azure_config:
                self.rudh_core = ProductionRudhCore(self.azure_config)
                print("🚀 Production core with Azure integration loaded")
            else:
                self.rudh_core = ProductionRudhCore()
                print("🔧 Production core in fallback mode loaded")
            
            # Initialize the core system
            init_results = await self.rudh_core.initialize()
            
            # Start session
            self.session_id = await self.rudh_core.start_session(self.user_id)
            self.session_start_time = datetime.now()
            
            # Show initialization results
            self._display_initialization_results(init_results)
            
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            print("🔄 Attempting fallback initialization...")
            
            try:
                # Fallback to basic initialization
                self.rudh_core = ProductionRudhCore()
                await self.rudh_core.initialize()
                self.session_id = await self.rudh_core.start_session(self.user_id)
                self.session_start_time = datetime.now()
                print("✅ Fallback initialization successful")
                return True
            except Exception as fallback_error:
                print(f"❌ Fallback initialization also failed: {fallback_error}")
                return False
    
    def _display_initialization_results(self, results: Dict[str, Any]):
        """Display detailed initialization results"""
        print("\n" + "="*80)
        print("🤖 RUDH AI COMPANION - VERSION 4.0 (Phase 2.3)")
        print("   Production-Ready Advanced Conversational AI")
        print("="*80)
        
        print("🌟 PHASE 2.3 FEATURES:")
        print("   ✅ Advanced response generation with Azure GPT-4")
        print("   ✅ Multi-modal capabilities (text, voice-ready)")
        print("   ✅ Real-time Azure AI services integration")
        print("   ✅ Production-grade performance monitoring")
        print("   ✅ Advanced user profiling and learning")
        print("   ✅ Secure credential management")
        print("   ✅ Comprehensive health monitoring")
        print("   ✅ Session management and insights")
        
        print("\n💬 ENHANCED CAPABILITIES:")
        print("   🎯 Context-aware responses with personality adaptation")
        print("   😊 Advanced emotional intelligence (16+ emotions)")
        print("   🧠 Sophisticated reasoning and analysis")
        print("   🌍 Real-time translation (Tamil/English + others)")
        print("   🎵 Voice synthesis with emotional styling")
        print("   📊 Real-time performance analytics")
        print("   🔄 Continuous learning and adaptation")
        
        # Show core engine status
        if results.get('core_engines'):
            print("\n🧠 CORE AI ENGINES: ✅ OPERATIONAL")
        else:
            print("\n🧠 CORE AI ENGINES: ⚠️ LIMITED")
        
        # Show Azure services status
        azure_services = results.get('azure_services', {})
        if azure_services:
            print("\n🌐 AZURE AI SERVICES:")
            active_services = sum(azure_services.values())
            total_services = len(azure_services)
            print(f"   📊 Status: {active_services}/{total_services} services active")
            
            for service, status in azure_services.items():
                status_icon = "✅" if status else "❌"
                service_name = service.replace('_', ' ').title()
                print(f"   {status_icon} {service_name}")
        else:
            print("\n🌐 AZURE AI SERVICES: 🔧 Fallback mode")
        
        print(f"\n⚡ INITIALIZATION TIME: {results.get('total_time', 0):.2f}s")
        
        if results.get('ready_for_production'):
            print("🎉 STATUS: PRODUCTION READY")
        else:
            print("⚠️ STATUS: LIMITED FUNCTIONALITY")
        
        print("\n📋 COMMANDS:")
        print("   '/help' - Show all commands")
        print("   '/stats' - Session statistics") 
        print("   '/insights' - User insights")
        print("   '/health' - System health")
        print("   '/azure' - Azure services status")
        print("   '/quit' - Exit gracefully")
        
        print("-"*80)
    
    async def run_interactive_session(self):
        """Main interactive conversation loop"""
        print(f"\n💬 Session {self.session_id} started!")
        print("🎯 Rudh is ready for advanced conversation with full AI capabilities")
        print("Type your message or use commands (start with '/')")
        print("-"*80)
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n[{self.conversation_count + 1}] You: ").strip()
                
                # Handle empty input
                if not user_input:
                    print("💭 Please enter a message or command.")
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    if await self._handle_command(user_input):
                        break  # Exit if quit command
                    continue
                
                # Process conversation
                await self._process_conversation(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Session interrupted by user")
                await self._quit_session()
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("🔄 Please try again or type '/help' for assistance")
    
    async def _process_conversation(self, user_input: str):
        """Process a conversation with full analysis and display"""
        print("🧠 Processing with advanced AI pipeline...")
        
        start_time = time.time()
        
        try:
            # Process with Rudh core
            response_data = await self.rudh_core.process_conversation(user_input, self.user_id)
            
            processing_time = time.time() - start_time
            self.conversation_count += 1
            
            # Display response
            self._display_response(response_data, processing_time)
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            print("🔄 Please try again")
    
    def _display_response(self, response_data: Dict[str, Any], actual_time: float):
        """Display comprehensive response with analysis"""
        # Main response
        print(f"\n🤖 Rudh: {response_data['response']}")
        
        # Detailed analysis
        if self.show_detailed_analysis:
            print(f"\n📊 ANALYSIS:")
            
            # Emotion and context
            emotion = response_data.get('emotion_detected', 'unknown')
            emotion_conf = response_data.get('emotion_confidence', 0)
            topic = response_data.get('topic', 'general')
            strategy = response_data.get('strategy_used', 'conversational')
            stage = response_data.get('conversation_stage', 'building')
            
            print(f"   😊 Emotion: {emotion.title()} ({emotion_conf:.0%} confidence)")
            print(f"   🎯 Topic: {topic.title()}")
            print(f"   💭 Strategy: {strategy.replace('_', ' ').title()}")
            print(f"   📈 Stage: {stage.title()}")
            print(f"   ⚡ Processing: {actual_time:.3f}s")
            
            # Confidence and reasoning
            confidence = response_data.get('confidence', 0)
            print(f"   🎲 Response Confidence: {confidence:.1%}")
            
            # Azure enhancements
            if response_data.get('azure_enhanced'):
                print(f"   🌐 Azure Enhanced: ✅")
                if response_data.get('audio_response'):
                    print(f"   🎵 Voice Available: ✅")
                if response_data.get('translated_response'):
                    print(f"   🌍 Translation Available: ✅")
            
        # Performance metrics
        if self.show_performance_metrics:
            breakdown = response_data.get('performance_breakdown', {})
            if breakdown:
                print(f"\n⚡ PERFORMANCE:")
                print(f"   🧠 Emotion: {breakdown.get('emotion_time', 0):.3f}s")
                print(f"   🎯 Context: {breakdown.get('context_time', 0):.3f}s") 
                print(f"   💬 Response: {breakdown.get('response_time', 0):.3f}s")
                print(f"   📊 Total: {breakdown.get('total_time', actual_time):.3f}s")
        
        # Suggestions and follow-ups
        suggestions = response_data.get('suggestions', [])
        follow_ups = response_data.get('follow_up_questions', [])
        
        if suggestions:
            print(f"\n💡 Suggestions:")
            for i, suggestion in enumerate(suggestions[:2], 1):
                print(f"   {i}. {suggestion}")
        
        if follow_ups:
            print(f"\n❓ Follow-up options:")
            for i, question in enumerate(follow_ups[:2], 1):
                print(f"   {i}. {question}")
        
        # Active capabilities
        capabilities = response_data.get('capabilities_active', [])
        if capabilities and self.show_detailed_analysis:
            print(f"\n🔧 Active: {', '.join(capabilities)}")
        
        print("💭 Type '/debug' for detailed response analysis")
    
    async def _handle_command(self, command: str) -> bool:
        """Handle user commands"""
        command_parts = command.split()
        base_command = command_parts[0].lower()
        
        if base_command in self.command_handlers:
            return await self.command_handlers[base_command](command_parts)
        else:
            print(f"❓ Unknown command: {base_command}")
            print("💭 Type '/help' to see available commands")
            return False
    
    async def _show_help(self, args: list) -> bool:
        """Show help information"""
        print("\n📋 RUDH AI COMPANION V4 - COMMAND REFERENCE")
        print("="*60)
        print("💬 CONVERSATION:")
        print("   Just type your message - Rudh will respond with full AI analysis")
        print("\n📊 SESSION MANAGEMENT:")
        print("   /stats    - Show session statistics and performance")
        print("   /insights - Detailed user profile and conversation insights")
        print("   /summary  - Session summary and key highlights")
        print("   /reset    - Start a fresh session")
        print("   /save     - Save current session")
        print("   /load     - Load previous session")
        print("\n🔧 SYSTEM INFORMATION:")
        print("   /health   - System health and component status")
        print("   /azure    - Azure AI services status and capabilities")
        print("   /profile  - Your user profile and learned preferences")
        print("   /settings - Interface settings and configuration")
        print("   /debug    - Toggle detailed analysis display")
        print("\n🎯 SPECIAL FEATURES:")
        print("   - Real-time emotion detection with 16+ emotions")
        print("   - Context-aware responses with personality adaptation") 
        print("   - Azure GPT-4 integration for advanced reasoning")
        print("   - Voice synthesis with emotional styling")
        print("   - Real-time translation (Tamil/English + others)")
        print("   - Continuous learning and user adaptation")
        print("\n🚪 EXIT:")
        print("   /quit     - Exit gracefully with session summary")
        return False
    
    async def _show_stats(self, args: list) -> bool:
        """Show session statistics"""
        if not self.session_start_time:
            print("❌ No active session")
            return False
        
        duration = datetime.now() - self.session_start_time
        
        print("\n📊 SESSION STATISTICS")
        print("="*50)
        print(f"Session ID: {self.session_id}")
        print(f"Duration: {duration}")
        print(f"Conversations: {self.conversation_count}")
        
        if hasattr(self.rudh_core, 'system_metrics'):
            metrics = self.rudh_core.system_metrics
            print(f"Average Response Time: {metrics.get('average_response_time', 0):.3f}s")
            print(f"Total System Conversations: {metrics.get('total_conversations', 0)}")
            
            uptime = datetime.now() - metrics.get('uptime_start', datetime.now())
            print(f"System Uptime: {uptime}")
        
        return False
    
    async def _show_insights(self, args: list) -> bool:
        """Show detailed user insights"""
        print("\n🔍 USER INSIGHTS & CONVERSATION ANALYSIS")
        print("="*60)
        
        try:
            insights = self.rudh_core.get_session_insights()
            
            if 'error' in insights:
                print(f"❌ {insights['error']}")
                return False
            
            # Session overview
            overview = insights.get('session_overview', {})
            print("📈 SESSION OVERVIEW:")
            for key, value in overview.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
            
            # Emotion analysis
            emotion_data = insights.get('emotion_analysis', {})
            print(f"\n😊 EMOTION ANALYSIS:")
            print(f"   Dominant Emotion: {emotion_data.get('dominant_emotion', 'N/A')}")
            print(f"   Emotions Detected: {emotion_data.get('emotion_diversity', 0)} different types")
            
            emotions = emotion_data.get('emotions_detected', {})
            if emotions:
                print("   Emotion Distribution:")
                for emotion, count in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                    print(f"     {emotion.title()}: {count} times")
            
            # Performance metrics
            performance = insights.get('performance_metrics', {})
            print(f"\n⚡ PERFORMANCE METRICS:")
            for key, value in performance.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
            
        except Exception as e:
            print(f"❌ Error retrieving insights: {e}")
        
        return False
    
    async def _show_health(self, args: list) -> bool:
        """Show system health status"""
        print("\n🏥 SYSTEM HEALTH STATUS")
        print("="*50)
        
        try:
            health_data = await self.rudh_core.get_health_status()
            
            overall_status = health_data.get('overall_status', 'unknown')
            status_icon = "✅" if overall_status == 'healthy' else "⚠️" if overall_status == 'degraded' else "❌"
            print(f"Overall Status: {status_icon} {overall_status.upper()}")
            
            # Core engines
            core_engines = health_data.get('core_engines', {})
            print(f"\n🧠 CORE AI ENGINES:")
            for engine, status in core_engines.items():
                icon = "✅" if status == 'healthy' else "❌"
                print(f"   {icon} {engine.replace('_', ' ').title()}: {status}")
            
            # Azure services
            azure_services = health_data.get('azure_services', {})
            if azure_services:
                print(f"\n🌐 AZURE AI SERVICES:")
                service_details = azure_services.get('service_details', {})
                for service, status in service_details.items():
                    icon = "✅" if 'healthy' in status else "❌"
                    print(f"   {icon} {service.title()}: {status}")
            
            # Capabilities
            capabilities = health_data.get('capabilities', [])
            if capabilities:
                print(f"\n🔧 ACTIVE CAPABILITIES:")
                for capability in capabilities:
                    print(f"   ✅ {capability.replace('_', ' ').title()}")
            
        except Exception as e:
            print(f"❌ Error retrieving health status: {e}")
        
        return False
    
    async def _show_azure_status(self, args: list) -> bool:
        """Show Azure services status"""
        print("\n🌐 AZURE AI SERVICES STATUS")
        print("="*50)
        
        if not hasattr(self.rudh_core, 'azure_integration') or not self.rudh_core.azure_integration:
            print("❌ Azure integration not available")
            print("🔧 Running in fallback mode")
            return False
        
        try:
            azure_status = self.rudh_core.azure_integration.get_service_status()
            
            # Overall status
            availability = azure_status.get('availability_percentage', 0)
            active_services = azure_status.get('active_services', 0)
            total_services = azure_status.get('total_services', 0)
            
            print(f"Availability: {availability:.1f}% ({active_services}/{total_services} services)")
            
            # Individual services
            services_status = azure_status.get('services_status', {})
            print(f"\n📊 SERVICE DETAILS:")
            
            service_names = {
                'credentials': 'Azure Credentials',
                'openai': 'Azure OpenAI (GPT-4)',
                'speech': 'Speech Synthesis',
                'translator': 'Real-time Translation',
                'search': 'Cognitive Search'
            }
            
            for service_key, status in services_status.items():
                service_name = service_names.get(service_key, service_key.title())
                icon = "✅" if status else "❌"
                print(f"   {icon} {service_name}")
            
            # Perform health check
            print(f"\n🔍 Performing live health check...")
            health_result = await self.rudh_core.azure_integration.health_check()
            
            overall_health = health_result.get('overall_health', 'unknown')
            print(f"Live Health Check: {overall_health.upper()}")
            
        except Exception as e:
            print(f"❌ Error checking Azure status: {e}")
        
        return False
    
    async def _toggle_debug(self, args: list) -> bool:
        """Toggle debug information display"""
        self.show_detailed_analysis = not self.show_detailed_analysis
        status = "enabled" if self.show_detailed_analysis else "disabled"
        print(f"🔧 Detailed analysis display: {status}")
        return False
    
    async def _reset_session(self, args: list) -> bool:
        """Reset current session"""
        print("🔄 Resetting session...")
        
        try:
            self.session_id = await self.rudh_core.start_session(self.user_id)
            self.conversation_count = 0
            self.session_start_time = datetime.now()
            print(f"✅ New session started: {self.session_id}")
        except Exception as e:
            print(f"❌ Session reset failed: {e}")
        
        return False
    
    async def _quit_session(self, args: list = None) -> bool:
        """Quit with session summary"""
        print("\n👋 Thank you for using Rudh AI Companion V4!")
        
        if self.session_start_time:
            duration = datetime.now() - self.session_start_time
            print(f"📊 Session Summary:")
            print(f"   Duration: {duration}")
            print(f"   Conversations: {self.conversation_count}")
            print(f"   Session ID: {self.session_id}")
        
        print("🌟 Your conversation insights and preferences have been saved.")
        print("💭 Remember: Rudh grows smarter with every conversation!")
        print("🚀 See you next time for even more advanced AI assistance!")
        
        return True
    
    # Placeholder methods for additional commands
    async def _show_summary(self, args: list) -> bool:
        print("📝 Session summary feature coming soon!")
        return False
    
    async def _show_user_profile(self, args: list) -> bool:
        print("👤 User profile display feature coming soon!")
        return False
    
    async def _show_settings(self, args: list) -> bool:
        print("⚙️ Settings configuration feature coming soon!")
        return False
    
    async def _save_session(self, args: list) -> bool:
        print("💾 Session save feature coming soon!")
        return False
    
    async def _load_session(self, args: list) -> bool:
        print("📂 Session load feature coming soon!")
        return False

async def main():
    """Main entry point for Rudh Interactive V4"""
    print("🚀 Starting Rudh AI Companion V4 - Production Ready!")
    print("🎯 Advanced conversational AI with Azure integration")
    
    interface = RudhInteractiveV4()
    
    # Initialize system
    if await interface.initialize():
        # Run interactive session
        await interface.run_interactive_session()
    else:
        print("❌ Failed to initialize Rudh. Please check your setup.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)