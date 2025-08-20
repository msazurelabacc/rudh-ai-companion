# interactive_creative_assistant.py
"""
Interactive Rudh Creative Assistant - Ready for Production Use
Natural language creative content generation
"""

import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Import the working creative engine
try:
    from creative_engine_working import CreativeEngine, WorkingAzureSpeechService
except ImportError:
    print("❌ Creative engine not found. Make sure creative_engine_working.py is available.")
    sys.exit(1)

class InteractiveCreativeAssistant:
    """Interactive Creative Assistant for Natural Language Content Creation"""
    
    def __init__(self):
        self.logger = logging.getLogger("InteractiveCreativeAssistant")
        
        # Initialize creative engine
        self.creative_engine = CreativeEngine()
        self.speech_service = WorkingAzureSpeechService()
        
        # Session tracking
        self.session_id = f"creative_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.query_count = 0
        self.created_content = []
        self.voice_enabled = True
        
        self.logger.info("✅ Interactive Creative Assistant initialized")
    
    async def speak_response(self, text: str):
        """Generate speech response"""
        if self.voice_enabled:
            try:
                await self.speech_service.speak_text(text)
            except Exception as e:
                print(f"🔊 Voice: {text}")
        else:
            print(f"🔊 Voice (disabled): {text}")
    
    async def start_interactive_session(self):
        """Start interactive creative session"""
        print("🚀 Initializing Interactive Rudh Creative Assistant...")
        
        await asyncio.sleep(0.5)
        
        print("================================================================================")
        print("🎨 RUDH INTERACTIVE CREATIVE ASSISTANT - READY FOR USE")
        print("   Natural Language Content Creation • Professional Outputs")
        print("================================================================================")
        print()
        print("🎯 CREATIVE CAPABILITIES:")
        print("   🎨 Visual Diagrams: ✅ PROFESSIONAL PNG GENERATION")
        print("   📊 Technical Diagrams: ✅ ARCHITECTURE, FLOWCHARTS, NETWORKS")
        print("   📋 Business Content: ✅ PRESENTATIONS, REPORTS, PROPOSALS")
        print("   🗣️ Voice Feedback: ✅ INTERACTIVE GUIDANCE")
        print("   📁 File Management: ✅ ORGANIZED OUTPUT DIRECTORY")
        print()
        print("🌟 PROVEN CAPABILITIES:")
        print("   ✅ Professional diagram generation (PNG format)")
        print("   ✅ Structured business content creation")
        print("   ✅ Natural language command processing")
        print("   ✅ Graceful fallback when services unavailable")
        print("   ✅ Enterprise-quality outputs")
        print()
        print("💬 HOW TO USE - NATURAL LANGUAGE COMMANDS:")
        print("   🎨 'Create an architecture diagram for my Azure AI system'")
        print("   📊 'Make a flowchart for user registration process'")
        print("   📋 'Generate a business presentation about AI portfolio management'")
        print("   📈 'Create a technical report on system performance'")
        print("   🖼️ 'Show me what I've created' (gallery)")
        print("   📚 'What templates are available?'")
        print()
        
        # Show current status
        files_created = len(list(self.creative_engine.output_dir.glob("*")))
        print(f"📊 Current Status: {files_created} files in creative gallery")
        print(f"💾 Output Directory: {self.creative_engine.output_dir}")
        print()
        
        # Start interactive loop
        await self._interactive_loop()
    
    async def _interactive_loop(self):
        """Main interactive loop"""
        print(f"💬 Creative session {self.session_id} started!")
        print("================================================================================")
        print("🎯 Ready for your creative requests! Use natural language to describe what you want.")
        print("   Type 'help' for examples, 'gallery' to see created content, 'quit' to exit")
        print("================================================================================")
        
        while True:
            try:
                # Get user input
                user_input = input("\n[🎨] What would you like to create? ").strip()
                
                if not user_input:
                    continue
                
                # Handle exit commands
                if user_input.lower() in ['/quit', '/exit', 'quit', 'exit', 'bye']:
                    print("\n👋 Thank you for using Rudh Creative Assistant!")
                    await self.speak_response("Thank you for using Rudh Creative Assistant! Keep creating amazing content!")
                    break
                
                # Process creative query
                start_time = time.time()
                await self._process_creative_request(user_input)
                processing_time = time.time() - start_time
                
                self.query_count += 1
                print(f"\n⚡ Request #{self.query_count} completed in {processing_time:.3f}s")
                
            except KeyboardInterrupt:
                print("\n\n👋 Creative session ended. Keep being creative!")
                break
            except Exception as e:
                self.logger.error(f"❌ Request processing error: {e}")
                print(f"❌ Error: {e}")
    
    async def _process_creative_request(self, request: str):
        """Process natural language creative requests"""
        try:
            request_lower = request.lower()
            
            # Architecture diagrams
            if any(word in request_lower for word in ['architecture', 'system diagram', 'system design']):
                await self._create_architecture_diagram(request)
            
            # Flowcharts and process diagrams
            elif any(word in request_lower for word in ['flowchart', 'process', 'workflow', 'flow']):
                await self._create_flowchart(request)
            
            # Network diagrams
            elif any(word in request_lower for word in ['network', 'topology', 'connections']):
                await self._create_network_diagram(request)
            
            # Business presentations
            elif any(word in request_lower for word in ['presentation', 'slides', 'pitch']):
                await self._create_presentation(request)
            
            # Reports and documentation
            elif any(word in request_lower for word in ['report', 'documentation', 'analysis']):
                await self._create_report(request)
            
            # Proposals
            elif any(word in request_lower for word in ['proposal', 'business plan', 'project plan']):
                await self._create_proposal(request)
            
            # Gallery and viewing content
            elif any(word in request_lower for word in ['gallery', 'show', 'created', 'files', 'list']):
                await self._show_gallery()
            
            # Templates
            elif any(word in request_lower for word in ['template', 'available', 'options']):
                await self._show_templates()
            
            # Help
            elif any(word in request_lower for word in ['help', 'examples', 'how to']):
                await self._show_help()
            
            # Voice toggle
            elif any(word in request_lower for word in ['voice', 'sound', 'audio']):
                await self._toggle_voice()
            
            # Stats and status
            elif any(word in request_lower for word in ['stats', 'status', 'info']):
                await self._show_stats()
            
            # Generic diagram request
            elif any(word in request_lower for word in ['diagram', 'chart', 'visual']):
                await self._create_generic_diagram(request)
            
            # Generic content request
            elif any(word in request_lower for word in ['create', 'generate', 'make']):
                await self._create_generic_content(request)
            
            # Conversational responses
            else:
                await self._handle_conversational_request(request)
                
        except Exception as e:
            self.logger.error(f"❌ Creative request processing failed: {e}")
            print(f"❌ Sorry, I encountered an error processing your request: {e}")
            print("💡 Try rephrasing your request or use 'help' for examples.")
    
    async def _create_architecture_diagram(self, request: str):
        """Create architecture diagram"""
        print("🏗️ Creating architecture diagram...")
        
        result = await self.creative_engine.generate_technical_diagram("architecture", request)
        
        if result['success']:
            print(f"✅ Architecture diagram created!")
            print(f"📁 File: {result['file_path']}")
            print(f"⚡ Generated in: {result['generation_time']}")
            
            self.created_content.append(result)
            
            await self.speak_response(f"Architecture diagram created successfully! Saved as {Path(result['file_path']).name}")
        else:
            print(f"❌ Failed to create architecture diagram: {result.get('error')}")
    
    async def _create_flowchart(self, request: str):
        """Create flowchart"""
        print("🔄 Creating flowchart...")
        
        result = await self.creative_engine.generate_technical_diagram("flowchart", request)
        
        if result['success']:
            print(f"✅ Flowchart created!")
            print(f"📁 File: {result['file_path']}")
            print(f"⚡ Generated in: {result['generation_time']}")
            
            self.created_content.append(result)
            
            await self.speak_response(f"Flowchart created successfully! Perfect for visualizing your process.")
        else:
            print(f"❌ Failed to create flowchart: {result.get('error')}")
    
    async def _create_network_diagram(self, request: str):
        """Create network diagram"""
        print("🌐 Creating network diagram...")
        
        result = await self.creative_engine.generate_technical_diagram("network", request)
        
        if result['success']:
            print(f"✅ Network diagram created!")
            print(f"📁 File: {result['file_path']}")
            
            self.created_content.append(result)
            
            await self.speak_response("Network diagram created successfully!")
        else:
            print(f"❌ Failed to create network diagram: {result.get('error')}")
    
    async def _create_presentation(self, request: str):
        """Create business presentation"""
        print("📊 Creating business presentation...")
        
        result = await self.creative_engine.generate_business_content("presentation", request)
        
        if result['success']:
            print(f"✅ Business presentation created!")
            print(f"📁 File: {result['file_path']}")
            print(f"📖 Preview: {result['content_preview']}")
            
            self.created_content.append(result)
            
            await self.speak_response("Professional business presentation created! Ready for your next meeting.")
        else:
            print(f"❌ Failed to create presentation: {result.get('error')}")
    
    async def _create_report(self, request: str):
        """Create technical report"""
        print("📋 Creating technical report...")
        
        result = await self.creative_engine.generate_business_content("report", request)
        
        if result['success']:
            print(f"✅ Technical report created!")
            print(f"📁 File: {result['file_path']}")
            
            self.created_content.append(result)
            
            await self.speak_response("Technical report generated with comprehensive analysis and recommendations.")
        else:
            print(f"❌ Failed to create report: {result.get('error')}")
    
    async def _create_proposal(self, request: str):
        """Create business proposal"""
        print("💼 Creating business proposal...")
        
        result = await self.creative_engine.generate_business_content("proposal", request)
        
        if result['success']:
            print(f"✅ Business proposal created!")
            print(f"📁 File: {result['file_path']}")
            
            self.created_content.append(result)
            
            await self.speak_response("Business proposal created with executive summary and implementation plan.")
        else:
            print(f"❌ Failed to create proposal: {result.get('error')}")
    
    async def _create_generic_diagram(self, request: str):
        """Create generic diagram based on request"""
        print("🎨 Analyzing your diagram request...")
        
        # Determine best diagram type
        if 'system' in request.lower() or 'architecture' in request.lower():
            diagram_type = "architecture"
        elif 'process' in request.lower() or 'flow' in request.lower():
            diagram_type = "flowchart"
        elif 'network' in request.lower():
            diagram_type = "network"
        else:
            diagram_type = "architecture"  # Default
        
        print(f"🎯 Creating {diagram_type} diagram...")
        
        result = await self.creative_engine.generate_technical_diagram(diagram_type, request)
        
        if result['success']:
            print(f"✅ {diagram_type.title()} diagram created!")
            print(f"📁 File: {result['file_path']}")
            
            self.created_content.append(result)
            
            await self.speak_response(f"{diagram_type.title()} diagram created successfully based on your request!")
    
    async def _create_generic_content(self, request: str):
        """Create generic content based on request"""
        print("📝 Analyzing your content request...")
        
        # Determine best content type
        if 'presentation' in request.lower() or 'slides' in request.lower():
            content_type = "presentation"
        elif 'report' in request.lower():
            content_type = "report"
        elif 'proposal' in request.lower():
            content_type = "proposal"
        else:
            content_type = "presentation"  # Default
        
        print(f"📋 Creating {content_type}...")
        
        result = await self.creative_engine.generate_business_content(content_type, request)
        
        if result['success']:
            print(f"✅ {content_type.title()} created!")
            print(f"📁 File: {result['file_path']}")
            
            self.created_content.append(result)
            
            await self.speak_response(f"Professional {content_type} created based on your specifications!")
    
    async def _show_gallery(self):
        """Show created content gallery"""
        files = list(self.creative_engine.output_dir.glob("*"))
        
        if not files:
            print("📭 Your creative gallery is empty. Start creating some amazing content!")
            await self.speak_response("Your gallery is empty. Let's create something amazing!")
            return
        
        print(f"\n🖼️ YOUR CREATIVE GALLERY ({len(files)} items)")
        print("=" * 60)
        
        # Group by type
        diagrams = [f for f in files if f.suffix in ['.png', '.svg'] or 'diagram' in f.name]
        content = [f for f in files if f.suffix in ['.md', '.txt'] and 'diagram' not in f.name]
        
        if diagrams:
            print(f"\n📊 DIAGRAMS ({len(diagrams)}):")
            for i, file in enumerate(sorted(diagrams, key=lambda x: x.stat().st_mtime, reverse=True), 1):
                print(f"   {i}. {file.name}")
        
        if content:
            print(f"\n📋 CONTENT ({len(content)}):")
            for i, file in enumerate(sorted(content, key=lambda x: x.stat().st_mtime, reverse=True), 1):
                print(f"   {i}. {file.name}")
        
        print(f"\n📁 Location: {self.creative_engine.output_dir}")
        
        await self.speak_response(f"Your gallery contains {len(files)} created items. Great work!")
    
    async def _show_templates(self):
        """Show available templates"""
        templates = await self.creative_engine.list_templates()
        
        print("\n📚 AVAILABLE CREATIVE TEMPLATES")
        print("=" * 50)
        
        diagram_templates = [t for t in templates if "Technical" in t['category']]
        content_templates = [t for t in templates if "Business" in t['category']]
        
        if diagram_templates:
            print("\n🎨 DIAGRAM TEMPLATES:")
            for template in diagram_templates:
                print(f"   ✅ {template['name']} - {template['description']}")
        
        if content_templates:
            print("\n📋 CONTENT TEMPLATES:")
            for template in content_templates:
                print(f"   ✅ {template['name']} - {template['description']}")
        
        print(f"\n💡 Simply describe what you want, and I'll use the appropriate template!")
        
        await self.speak_response(f"I have {len(templates)} professional templates ready for your creative projects!")
    
    async def _show_help(self):
        """Show help and examples"""
        help_text = """
🎨 RUDH CREATIVE ASSISTANT - NATURAL LANGUAGE EXAMPLES

🏗️ ARCHITECTURE DIAGRAMS:
   • "Create an architecture diagram for my Azure AI system"
   • "Show me a system design for e-commerce platform"
   • "Design the architecture for microservices app"

🔄 FLOWCHARTS & PROCESSES:
   • "Make a flowchart for user registration process"
   • "Create a workflow for customer onboarding"
   • "Show the decision flow for loan approval"

📊 BUSINESS PRESENTATIONS:
   • "Generate a presentation about AI portfolio management"
   • "Create slides for quarterly business review"
   • "Make a pitch deck for startup funding"

📋 REPORTS & DOCUMENTATION:
   • "Write a technical report on system performance"
   • "Create documentation for API integration"
   • "Generate analysis report for market research"

💼 BUSINESS PROPOSALS:
   • "Create a proposal for AI implementation project"
   • "Make a business plan for new product launch"
   • "Generate project proposal for digital transformation"

🖼️ GALLERY & MANAGEMENT:
   • "Show me what I've created" or "gallery"
   • "What templates are available?"
   • "Show my recent files"

🎯 TIPS FOR BEST RESULTS:
   ✅ Be specific about your needs
   ✅ Mention the context (e.g., "for Chennai market")
   ✅ Include key components you want
   ✅ Specify the audience or purpose

💡 JUST DESCRIBE WHAT YOU WANT IN NATURAL LANGUAGE!
        """
        print(help_text)
        
        await self.speak_response("Help examples displayed! Just describe what you want to create in natural language.")
    
    async def _toggle_voice(self):
        """Toggle voice synthesis"""
        self.voice_enabled = not self.voice_enabled
        status = "enabled" if self.voice_enabled else "disabled"
        print(f"🔊 Voice synthesis {status}")
        
        if self.voice_enabled:
            await self.speak_response("Voice synthesis enabled for creative feedback")
    
    async def _show_stats(self):
        """Show session statistics"""
        files = list(self.creative_engine.output_dir.glob("*"))
        
        print("\n📊 CREATIVE SESSION STATISTICS")
        print("=" * 40)
        print(f"🎯 Session ID: {self.session_id}")
        print(f"📈 Requests processed: {self.query_count}")
        print(f"📁 Files created: {len(files)}")
        print(f"🎨 Graphics enabled: ✅ Yes")
        print(f"🗣️ Voice synthesis: {'✅ Enabled' if self.voice_enabled else '❌ Disabled'}")
        print(f"💾 Output directory: {self.creative_engine.output_dir}")
        
        if files:
            print(f"\n📄 Recent files:")
            for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
                print(f"   • {file.name}")
        
        await self.speak_response(f"Session statistics: {self.query_count} requests processed, {len(files)} files created.")
    
    async def _handle_conversational_request(self, request: str):
        """Handle conversational requests"""
        print("💬 I understand you want to create something!")
        print()
        print("🎯 Here are some things I can help you create:")
        print("   🏗️ Architecture diagrams (system designs, cloud architectures)")
        print("   🔄 Flowcharts (processes, workflows, decision trees)")
        print("   🌐 Network diagrams (connections, topologies)")
        print("   📊 Business presentations (slides, pitch decks)")
        print("   📋 Technical reports (analysis, documentation)")
        print("   💼 Business proposals (project plans, business cases)")
        print()
        print("💡 Try saying something like:")
        print("   'Create an architecture diagram for my project'")
        print("   'Make a presentation about AI portfolio management'")
        print("   'Generate a flowchart for user onboarding'")
        
        await self.speak_response("I can create many types of content for you! Try describing what you need in natural language.")

# Main execution
async def main():
    """Main function to start the interactive creative assistant"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Create and start interactive assistant
        assistant = InteractiveCreativeAssistant()
        await assistant.start_interactive_session()
        
    except KeyboardInterrupt:
        print("\n👋 Creative session ended.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Interactive Rudh Creative Assistant...")
    asyncio.run(main())