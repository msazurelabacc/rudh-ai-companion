# rudh_creative_assistant_v41.py
"""
Rudh Creative Assistant V4.1 - Phase 4.1 Complete System
Voice-enabled content creation with AI-powered intelligence
"""

import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Import core creative engine
try:
    from creative_engine_core import CreativeEngine
except ImportError:
    print("❌ Creative Engine not found. Make sure creative_engine_core.py is available.")
    sys.exit(1)

# Import existing Rudh components
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from azure_openai_service import AzureOpenAIService
    from azure_speech_service import AzureSpeechService
except ImportError:
    # Fallback classes
    class AzureOpenAIService:
        def __init__(self):
            self.logger = logging.getLogger("AzureOpenAI")
            self.logger.warning("⚠️ Azure OpenAI service not available")
        
        async def get_response(self, prompt):
            return "AI service not available. Using creative templates."
    
    class AzureSpeechService:
        def __init__(self):
            self.logger = logging.getLogger("AzureSpeech")
            self.logger.warning("⚠️ Azure Speech service not available")
        
        async def speak_text(self, text):
            print(f"🔊 Voice: {text}")


class RudhCreativeAssistant:
    """Enhanced Creative Assistant with Voice Integration"""
    
    def __init__(self):
        self.logger = logging.getLogger("RudhCreativeAssistant")
        
        # Initialize core creative engine
        self.creative_engine = CreativeEngine()
        
        # Initialize AI services
        self.ai_service = None
        self.speech_service = None
        self.voice_enabled = False
        
        # Session tracking
        self.session_id = f"creative_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.query_count = 0
        self.created_content = []
        
        # Initialize AI services asynchronously
        asyncio.create_task(self._init_ai_services())
    
    async def _init_ai_services(self):
        """Initialize AI services"""
        try:
            # Initialize Azure OpenAI
            self.ai_service = AzureOpenAIService()
            self.logger.info("✅ Azure OpenAI service initialized")
            
            # Initialize Azure Speech
            self.speech_service = AzureSpeechService()
            self.voice_enabled = True
            self.logger.info("✅ Azure Speech service initialized")
            
        except Exception as e:
            self.logger.warning(f"⚠️ AI services initialization failed: {e}")
            self.voice_enabled = False
    
    async def speak_response(self, text: str):
        """Generate speech for response if voice enabled"""
        if self.voice_enabled and self.speech_service:
            try:
                start_time = time.time()
                
                # Smart method detection for speech service
                if hasattr(self.speech_service, 'speak_text'):
                    await self.speech_service.speak_text(text)
                elif hasattr(self.speech_service, 'text_to_speech'):
                    await self.speech_service.text_to_speech(text)
                elif hasattr(self.speech_service, 'synthesize_speech'):
                    await self.speech_service.synthesize_speech(text)
                else:
                    print(f"🔊 Voice (fallback): {text}")
                    return
                
                speech_time = time.time() - start_time
                print(f"🎵 Speech completed ({speech_time:.3f}s)")
                
            except Exception as e:
                self.logger.warning(f"Speech synthesis failed: {e}")
                print(f"🔊 Voice (fallback): {text}")
        else:
            print(f"🔊 Voice (disabled): {text}")
    
    async def start_interactive_session(self):
        """Start interactive creative assistant session"""
        print("🚀 Initializing Rudh Creative Assistant V4.1...")
        
        # Allow AI services to initialize
        await asyncio.sleep(1)
        
        print("================================================================================")
        print("🎨 RUDH CREATIVE ASSISTANT V4.1 - AI-POWERED CONTENT CREATION")
        print("   Technical Diagrams • Business Content • Voice Enhancement")
        print("================================================================================")
        print()
        print("🧠 CREATIVE ENGINES:")
        print("   🎨 Content Creation: ✅ TECHNICAL DIAGRAMS & BUSINESS CONTENT")
        print("   📊 Diagram Generation: ✅ ARCHITECTURE, FLOWCHARTS, NETWORKS")
        print("   📋 Business Content: ✅ PRESENTATIONS, REPORTS, PROPOSALS")
        print("   🤖 Azure OpenAI (GPT-4o): ✅ CONNECTED" if self.ai_service else "   🤖 Azure OpenAI: ❌ OFFLINE")
        print("   🗣️ Voice Synthesis: ✅ ENABLED" if self.voice_enabled else "   🗣️ Voice Synthesis: ❌ DISABLED")
        print("   🎯 Graphics Engine: ✅ ADVANCED VISUALS" if self.creative_engine.graphics_enabled else "   🎯 Graphics Engine: ❌ TEXT MODE")
        print()
        print("🌟 NEW IN V4.1:")
        print("   ✅ AI-Powered Diagram Generation (Architecture, Flow, Network)")
        print("   ✅ Professional Business Content Creation")
        print("   ✅ Voice-Guided Creative Process")
        print("   ✅ Chennai Business Context Integration")
        print("   ✅ Multiple Export Formats (SVG, PDF, Markdown)")
        print("   ✅ Professional Template Library")
        print()
        print("💬 Welcome to your creative assistant! I can help you with:")
        print("   • Technical diagram creation (architecture, flowcharts, networks)")
        print("   • Business content generation (presentations, reports, proposals)")
        print("   • Professional template selection and customization")
        print("   • Voice-guided creative workflow")
        print("   • Chennai business context optimization")
        print()
        print("🎨 EXAMPLE COMMANDS:")
        print("   create diagram architecture      - Generate system architecture diagram")
        print("   create content presentation     - Create business presentation")
        print("   templates                       - Show available templates")
        print("   gallery                         - View created content")
        print("   /stats                          - Creative engine statistics")
        print()
        
        # Start interactive loop
        await self._interactive_loop()
    
    async def _interactive_loop(self):
        """Main interactive loop"""
        print(f"💬 Creative session {self.session_id} started!")
        print("--------------------------------------------------------------------------------")
        
        while True:
            try:
                # Get user input
                user_input = input("\n[🎨] Your creative request: ").strip()
                
                if not user_input:
                    continue
                
                # Handle exit commands
                if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                    print("\n👋 Thank you for using Rudh Creative Assistant!")
                    await self.speak_response("Thank you for using Rudh Creative Assistant!")
                    break
                
                # Process creative query
                start_time = time.time()
                await self._process_creative_query(user_input)
                processing_time = time.time() - start_time
                
                self.query_count += 1
                print(f"\n⚡ Creative request #{self.query_count} completed in {processing_time:.3f}s")
                
            except KeyboardInterrupt:
                print("\n\n👋 Creative session ended. Keep creating!")
                break
            except Exception as e:
                self.logger.error(f"❌ Query processing error: {e}")
                print(f"❌ Error: {e}")
    
    async def _process_creative_query(self, query: str):
        """Process creative assistant queries"""
        try:
            query_lower = query.lower()
            
            # Create technical diagrams
            if query_lower.startswith('create diagram '):
                diagram_type = query.split(' ', 2)[2] if len(query.split(' ')) > 2 else 'architecture'
                await self._handle_diagram_creation(diagram_type, query)
            
            # Create business content
            elif query_lower.startswith('create content '):
                content_type = query.split(' ', 2)[2] if len(query.split(' ')) > 2 else 'presentation'
                await self._handle_content_creation(content_type, query)
            
            # Quick diagram creation
            elif any(word in query_lower for word in ['diagram', 'flowchart', 'architecture']):
                await self._handle_quick_diagram(query)
            
            # Quick content creation
            elif any(word in query_lower for word in ['presentation', 'report', 'proposal']):
                await self._handle_quick_content(query)
            
            # Show templates
            elif query_lower in ['templates', 'template', 'list templates']:
                await self._handle_templates()
            
            # Show gallery/created content
            elif query_lower in ['gallery', 'show gallery', 'created', 'files']:
                await self._handle_gallery()
            
            # Creative statistics
            elif query_lower in ['/stats', 'stats', 'statistics']:
                await self._handle_stats()
            
            # Voice toggle
            elif query_lower in ['/voice', 'voice']:
                await self._toggle_voice()
            
            # Help
            elif query_lower in ['/help', 'help']:
                await self._show_help()
            
            # AI-powered general creative query
            else:
                await self._handle_ai_creative_query(query)
                
        except Exception as e:
            self.logger.error(f"❌ Creative query processing failed: {e}")
            print(f"❌ Sorry, I encountered an error: {e}")
    
    async def _handle_diagram_creation(self, diagram_type: str, full_query: str):
        """Handle technical diagram creation"""
        try:
            print(f"🎨 Creating {diagram_type} diagram...")
            
            # Get detailed specification
            specification = input(f"📝 Describe your {diagram_type} diagram: ").strip()
            if not specification:
                specification = f"Create a professional {diagram_type} diagram based on the request: {full_query}"
            
            # Generate diagram
            result = await self.creative_engine.generate_technical_diagram(diagram_type, specification)
            
            if result['success']:
                print(f"\n✅ DIAGRAM CREATED SUCCESSFULLY!")
                print(f"📁 File: {result['file_path']}")
                print(f"🎯 Type: {result['diagram_type']}")
                print(f"⚡ Generation time: {result['generation_time']}")
                
                # Add to created content
                self.created_content.append({
                    "type": "diagram",
                    "subtype": diagram_type,
                    "file": result['file_path'],
                    "timestamp": result['timestamp']
                })
                
                voice_response = f"Successfully created {diagram_type} diagram. File saved as {Path(result['file_path']).name}"
                await self.speak_response(voice_response)
                
            else:
                print(f"❌ Diagram creation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Diagram creation error: {e}")
    
    async def _handle_content_creation(self, content_type: str, full_query: str):
        """Handle business content creation"""
        try:
            print(f"📋 Creating {content_type} content...")
            
            # Get detailed specification
            specification = input(f"📝 Describe your {content_type} requirements: ").strip()
            if not specification:
                specification = f"Create professional {content_type} content based on: {full_query}"
            
            # Generate content
            result = await self.creative_engine.generate_business_content(content_type, specification)
            
            if result['success']:
                print(f"\n✅ CONTENT CREATED SUCCESSFULLY!")
                print(f"📁 File: {result['file_path']}")
                print(f"🎯 Type: {result['content_type']}")
                print(f"⚡ Generation time: {result['generation_time']}")
                print(f"📖 Preview: {result['content_preview']}")
                
                # Add to created content
                self.created_content.append({
                    "type": "content",
                    "subtype": content_type,
                    "file": result['file_path'],
                    "timestamp": result['timestamp']
                })
                
                voice_response = f"Successfully created {content_type} content. File saved and ready for use."
                await self.speak_response(voice_response)
                
            else:
                print(f"❌ Content creation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Content creation error: {e}")
    
    async def _handle_quick_diagram(self, query: str):
        """Handle quick diagram creation from natural language"""
        try:
            print("🎨 Analyzing your diagram request...")
            
            # Determine diagram type from query
            if 'architecture' in query.lower():
                diagram_type = 'architecture'
            elif 'flow' in query.lower() or 'process' in query.lower():
                diagram_type = 'flowchart'
            elif 'network' in query.lower():
                diagram_type = 'network'
            elif 'database' in query.lower():
                diagram_type = 'database'
            else:
                diagram_type = 'architecture'  # Default
            
            # Use the query as specification
            result = await self.creative_engine.generate_technical_diagram(diagram_type, query)
            
            if result['success']:
                print(f"\n✅ QUICK DIAGRAM CREATED!")
                print(f"📁 File: {result['file_path']}")
                print(f"🎯 Detected type: {diagram_type}")
                
                self.created_content.append({
                    "type": "diagram",
                    "subtype": diagram_type,
                    "file": result['file_path'],
                    "timestamp": result['timestamp']
                })
                
                voice_response = f"Quick {diagram_type} diagram created successfully."
                await self.speak_response(voice_response)
                
        except Exception as e:
            print(f"❌ Quick diagram creation error: {e}")
    
    async def _handle_quick_content(self, query: str):
        """Handle quick content creation from natural language"""
        try:
            print("📋 Analyzing your content request...")
            
            # Determine content type from query
            if 'presentation' in query.lower():
                content_type = 'presentation'
            elif 'report' in query.lower():
                content_type = 'report'
            elif 'proposal' in query.lower():
                content_type = 'proposal'
            elif 'marketing' in query.lower():
                content_type = 'marketing'
            else:
                content_type = 'presentation'  # Default
            
            # Use the query as specification
            result = await self.creative_engine.generate_business_content(content_type, query)
            
            if result['success']:
                print(f"\n✅ QUICK CONTENT CREATED!")
                print(f"📁 File: {result['file_path']}")
                print(f"🎯 Detected type: {content_type}")
                print(f"📖 Preview: {result['content_preview']}")
                
                self.created_content.append({
                    "type": "content",
                    "subtype": content_type,
                    "file": result['file_path'],
                    "timestamp": result['timestamp']
                })
                
                voice_response = f"Quick {content_type} content created successfully."
                await self.speak_response(voice_response)
                
        except Exception as e:
            print(f"❌ Quick content creation error: {e}")
    
    async def _handle_templates(self):
        """Handle template listing"""
        try:
            print("📚 Loading available templates...")
            
            templates = await self.creative_engine.list_templates()
            
            print("\n📚 AVAILABLE CREATIVE TEMPLATES")
            print("=" * 50)
            
            current_category = ""
            for template in templates:
                if template['category'] != current_category:
                    current_category = template['category']
                    print(f"\n🎯 {current_category}:")
                
                status = "✅" if template['available'] else "❌"
                print(f"   {status} {template['name']} ({template['type']})")
                print(f"      {template['description']}")
            
            print(f"\n📊 Total templates: {len(templates)}")
            
            voice_response = f"Found {len(templates)} creative templates across multiple categories."
            await self.speak_response(voice_response)
            
        except Exception as e:
            print(f"❌ Template listing error: {e}")
    
    async def _handle_gallery(self):
        """Handle created content gallery"""
        try:
            print("🖼️ Loading your creative gallery...")
            
            if not self.created_content:
                print("\n📭 Your gallery is empty. Create some content first!")
                await self.speak_response("Your creative gallery is empty. Start creating some amazing content!")
                return
            
            print("\n🖼️ YOUR CREATIVE GALLERY")
            print("=" * 40)
            
            # Group by type
            diagrams = [item for item in self.created_content if item['type'] == 'diagram']
            content = [item for item in self.created_content if item['type'] == 'content']
            
            if diagrams:
                print(f"\n📊 Technical Diagrams ({len(diagrams)}):")
                for i, item in enumerate(diagrams, 1):
                    file_name = Path(item['file']).name
                    print(f"   {i}. {item['subtype'].title()} - {file_name}")
            
            if content:
                print(f"\n📋 Business Content ({len(content)}):")
                for i, item in enumerate(content, 1):
                    file_name = Path(item['file']).name
                    print(f"   {i}. {item['subtype'].title()} - {file_name}")
            
            print(f"\n📊 Total created: {len(self.created_content)} items")
            
            voice_response = f"Your gallery contains {len(self.created_content)} created items."
            await self.speak_response(voice_response)
            
        except Exception as e:
            print(f"❌ Gallery display error: {e}")
    
    async def _handle_stats(self):
        """Handle creative statistics"""
        try:
            print("📊 Generating creative statistics...")
            
            stats = await self.creative_engine.get_creative_stats()
            
            print("\n📊 CREATIVE ENGINE STATISTICS")
            print("=" * 40)
            print(f"📈 Session queries: {self.query_count}")
            print(f"🎨 Total created: {stats.get('total_created', 0)}")
            print(f"🎯 Graphics engine: {'✅ Enabled' if stats.get('graphics_enabled') else '❌ Disabled'}")
            print(f"🤖 AI service: {stats.get('ai_service_status', 'unknown')}")
            print(f"📚 Templates: {stats.get('templates_available', 0)}")
            print(f"📁 Output directory: {stats.get('output_directory', 'unknown')}")
            print(f"💬 Session ID: {self.session_id}")
            print(f"🗣️ Voice synthesis: {'✅ Enabled' if self.voice_enabled else '❌ Disabled'}")
            
            if stats.get('recent_files'):
                print(f"\n📄 Recent files:")
                for file in stats['recent_files']:
                    print(f"   • {file}")
            
            voice_response = f"Creative session statistics: {self.query_count} queries processed, {stats.get('total_created', 0)} items created."
            await self.speak_response(voice_response)
            
        except Exception as e:
            print(f"❌ Statistics error: {e}")
    
    async def _toggle_voice(self):
        """Toggle voice synthesis"""
        try:
            if self.speech_service:
                self.voice_enabled = not self.voice_enabled
                status = "enabled" if self.voice_enabled else "disabled"
                print(f"🔊 Voice synthesis {status}")
                
                if self.voice_enabled:
                    await self.speak_response("Voice synthesis enabled for creative workflow")
            else:
                print("❌ Voice synthesis not available")
                
        except Exception as e:
            print(f"❌ Voice toggle failed: {e}")
    
    async def _show_help(self):
        """Show help information"""
        help_text = """
🎨 RUDH CREATIVE ASSISTANT V4.1 - HELP

📊 DIAGRAM CREATION:
   • create diagram [type]     - Create technical diagrams
     Examples: create diagram architecture
               create diagram flowchart

📋 CONTENT CREATION:
   • create content [type]     - Create business content
     Examples: create content presentation
               create content report

🚀 QUICK CREATION:
   • Natural language requests - Just describe what you want!
     Examples: "architecture diagram for my Azure system"
               "presentation about AI portfolio management"

📚 TEMPLATES & GALLERY:
   • templates                 - Show available templates
   • gallery                   - View your created content
   • /stats                    - Creative engine statistics

🔧 SYSTEM COMMANDS:
   • /voice                    - Toggle voice synthesis
   • /help                     - Show this help
   • /quit                     - Exit creative assistant

🎯 DIAGRAM TYPES:
   ✅ Architecture diagrams (systems, cloud, technical)
   ✅ Flowcharts (processes, workflows, decisions)
   ✅ Network diagrams (connections, topology)
   ✅ Database schemas (relationships, structures)

📋 CONTENT TYPES:
   ✅ Business presentations (professional slides)
   ✅ Technical reports (documentation, analysis)
   ✅ Project proposals (business cases, plans)
   ✅ Marketing materials (content, campaigns)

🌟 ENHANCED FEATURES:
   ✅ AI-powered content analysis and generation
   ✅ Voice-guided creative workflow
   ✅ Chennai business context optimization
   ✅ Professional template library
   ✅ Multiple export formats (SVG, PDF, Markdown)
        """
        print(help_text)
        
        await self.speak_response("Creative assistant help displayed. Use natural language to describe what you want to create!")
    
    async def _handle_ai_creative_query(self, query: str):
        """Handle AI-powered general creative queries"""
        try:
            if not self.ai_service:
                print("❌ AI service not available. Please use specific commands.")
                print("💡 Try: 'create diagram architecture', 'create content presentation', 'templates'")
                return
            
            print("🧠 Processing creative request with AI...")
            
            # Create context for AI
            context = """You are Rudh, an advanced AI creative assistant specializing in technical diagrams and business content creation. 
            You help users create professional diagrams, presentations, reports, and other business content. 
            You have expertise in Chennai business context and can suggest appropriate creative solutions.
            Provide helpful, actionable creative guidance. Be concise but informative."""
            
            enhanced_prompt = f"{context}\n\nUser creative request: {query}"
            
            # Get AI response
            response = await self.ai_service.get_response(enhanced_prompt)
            
            print(f"🤖 Rudh: {response}")
            
            # Voice synthesis
            voice_summary = f"AI creative analysis complete for your request about {query.split()[0] if query.split() else 'content creation'}."
            await self.speak_response(voice_summary)
            
        except Exception as e:
            print(f"❌ AI creative query failed: {e}")
            # Provide helpful fallback
            print("💡 Try these creative commands:")
            print("   • create diagram architecture - Technical system diagrams")
            print("   • create content presentation - Business presentations")
            print("   • templates - Show available templates")
            print("   • gallery - View your created content")


# Main execution
async def main():
    """Main function to start the creative assistant"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Create and start creative assistant
        assistant = RudhCreativeAssistant()
        await assistant.start_interactive_session()
        
    except KeyboardInterrupt:
        print("\n👋 Creative session ended.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    print("🚀 Starting Rudh Creative Assistant V4.1...")
    asyncio.run(main())