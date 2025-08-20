# rudh_video_assistant_v42.py
"""
Rudh Video Assistant V4.2 - Interactive AI-Powered Video Creation
Creates professional videos with voice narration and Chennai business context
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Import video engine
try:
    from video_engine_core import VideoEngine
    VIDEO_ENGINE_AVAILABLE = True
except ImportError:
    VIDEO_ENGINE_AVAILABLE = False

# Azure services for voice feedback
try:
    from azure_speechservice import AzureSpeechService
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

class RudhVideoAssistant:
    """Interactive AI Video Creation Assistant"""
    
    def __init__(self):
        print("🎬 Starting Rudh Video Assistant V4.2...")
        
        # Initialize video engine
        if VIDEO_ENGINE_AVAILABLE:
            self.video_engine = VideoEngine()
            print("✅ Video Engine loaded successfully")
        else:
            self.video_engine = None
            print("❌ Video Engine not available - using simulation mode")
        
        # Initialize speech service
        if SPEECH_AVAILABLE:
            try:
                self.speech_service = AzureSpeechService()
                if hasattr(self.speech_service, 'is_available') and self.speech_service.is_available():
                    print("✅ Azure Speech Service connected")
                else:
                    print("⚠️ Azure Speech Service not available")
                    self.speech_service = None
            except Exception as e:
                print(f"⚠️ Speech service error: {e}")
                self.speech_service = None
        else:
            self.speech_service = None
        
        # Video creation statistics
        self.stats = {
            'videos_created': 0,
            'total_duration': 0,
            'slides_generated': 0,
            'audio_files_created': 0,
            'session_start': datetime.now()
        }
        
        # Video templates
        self.video_templates = {
            'explainer': {
                'description': 'Educational video explaining concepts clearly',
                'duration': 180,  # 3 minutes
                'style': 'professional',
                'audience': 'Business professionals'
            },
            'presentation': {
                'description': 'Business presentation with key points',
                'duration': 300,  # 5 minutes
                'style': 'corporate',
                'audience': 'Stakeholders and executives'
            },
            'tutorial': {
                'description': 'Step-by-step instructional video',
                'duration': 420,  # 7 minutes
                'style': 'educational',
                'audience': 'Learners and implementers'
            },
            'social': {
                'description': 'Short engaging content for social media',
                'duration': 60,  # 1 minute
                'style': 'dynamic',
                'audience': 'General public'
            },
            'pitch': {
                'description': 'Compelling business pitch or proposal',
                'duration': 240,  # 4 minutes
                'style': 'persuasive',
                'audience': 'Investors and clients'
            }
        }
        
        print("\n🎥 RUDH VIDEO ASSISTANT V4.2 - AI-POWERED VIDEO CREATION")
        print("=" * 65)
        print("🎯 CREATE PROFESSIONAL VIDEOS WITH AI INTELLIGENCE")
        print("🗣️ VOICE-ENHANCED WORKFLOW WITH INDIAN ENGLISH")
        print("🏢 CHENNAI BUSINESS CONTEXT & TAMIL MARKET INSIGHTS")
        print("=" * 65)
        
    def provide_voice_feedback(self, message: str):
        """Provide voice feedback if available"""
        if self.speech_service:
            try:
                # Try different speech methods
                for method_name in ['speak_text', 'text_to_speech', 'synthesize_speech']:
                    if hasattr(self.speech_service, method_name):
                        try:
                            start_time = time.time()
                            result = getattr(self.speech_service, method_name)(
                                message, "en-IN-NeerjaNeural"
                            )
                            if result:
                                duration = time.time() - start_time
                                audio_size = len(result.audio_data) if hasattr(result, 'audio_data') else len(str(result))
                                print(f"🗣️ Voice feedback delivered ({duration:.3f}s, {audio_size:,} bytes)")
                                return
                        except Exception as e:
                            continue
                print("⚠️ Voice synthesis unavailable")
            except Exception as e:
                print(f"⚠️ Voice feedback error: {e}")
    
    def create_video(self, topic: str, video_type: str = "explainer", 
                    duration: int = None, theme: str = "tech") -> str:
        """Create professional video with AI intelligence"""
        
        # Get template info
        template = self.video_templates.get(video_type, self.video_templates["explainer"])
        if duration is None:
            duration = template['duration']
        
        print(f"\n🎬 CREATING {video_type.upper()} VIDEO")
        print(f"📝 Topic: {topic}")
        print(f"⏱️ Duration: {duration} seconds")
        print(f"🎨 Theme: {theme}")
        print(f"👥 Audience: {template['audience']}")
        
        # Voice feedback
        self.provide_voice_feedback(f"Creating {video_type} video about {topic}. This will be excellent!")
        
        if self.video_engine:
            try:
                print("\n📋 Step 1: Generating AI-powered script...")
                start_time = time.time()
                
                script = self.video_engine.create_video_script(topic, video_type, duration)
                script_time = time.time() - start_time
                
                print(f"✅ Script generated in {script_time:.2f}s")
                print(f"📊 Title: {script.get('title', 'Untitled')}")
                print(f"🎬 Scenes: {len(script.get('scenes', []))}")
                
                print("\n🎥 Step 2: Creating video assets...")
                asset_start = time.time()
                
                result = self.video_engine.create_simple_video(script, theme)
                asset_time = time.time() - asset_start
                
                if result:
                    # Update statistics
                    self.stats['videos_created'] += 1
                    self.stats['total_duration'] += duration
                    self.stats['slides_generated'] += len(script.get('scenes', []))
                    
                    total_time = time.time() - start_time
                    
                    print(f"\n🎉 VIDEO CREATION SUCCESSFUL!")
                    print(f"📁 Output: {os.path.basename(result)}")
                    print(f"⏱️ Total time: {total_time:.2f}s")
                    print(f"📊 Performance: {len(script.get('scenes', []))/total_time:.1f} scenes/second")
                    
                    # Voice success feedback
                    self.provide_voice_feedback(f"Video about {topic} created successfully! Professional quality content ready for use.")
                    
                    return result
                else:
                    print("❌ Video creation failed")
                    return None
                    
            except Exception as e:
                print(f"❌ Video creation error: {e}")
                return None
        else:
            # Simulation mode
            print("\n🔄 SIMULATION MODE - Video Engine Not Available")
            print("📝 Would create professional video with:")
            print(f"   • {duration//30} high-quality slides")
            print(f"   • AI-generated narration in Indian English")
            print(f"   • {theme} theme with Chennai business context")
            print(f"   • Professional {template['style']} styling")
            
            # Simulate creation time
            time.sleep(2)
            print("✅ Simulation complete - video would be created successfully!")
            
            # Voice feedback
            self.provide_voice_feedback(f"Video simulation completed for {topic}. Ready for actual creation when video engine is available!")
            
            return "simulation_complete"
    
    def show_templates(self):
        """Display available video templates"""
        print("\n📋 AVAILABLE VIDEO TEMPLATES")
        print("=" * 50)
        
        for template_type, info in self.video_templates.items():
            duration_min = info['duration'] // 60
            duration_sec = info['duration'] % 60
            print(f"\n🎬 {template_type.upper()}")
            print(f"   📝 {info['description']}")
            print(f"   ⏱️ Duration: {duration_min}m {duration_sec}s")
            print(f"   🎨 Style: {info['style']}")
            print(f"   👥 Audience: {info['audience']}")
    
    def show_gallery(self):
        """Show created videos gallery"""
        print("\n🖼️ VIDEO GALLERY")
        print("=" * 30)
        
        if self.video_engine:
            output_dir = self.video_engine.video_output_dir
            if output_dir.exists():
                video_files = list(output_dir.glob("video_*.mp4")) + list(output_dir.glob("video_info_*.json"))
                
                if video_files:
                    print(f"📁 Location: {output_dir}")
                    for file in sorted(video_files):
                        file_size = os.path.getsize(file) if file.exists() else 0
                        size_mb = file_size / (1024 * 1024)
                        print(f"   📹 {file.name} ({size_mb:.1f} MB)")
                else:
                    print("   📭 No videos created yet")
            else:
                print("   📁 Gallery directory not found")
        else:
            print("   🔄 Video engine not available")
        
        print(f"\n📊 SESSION STATISTICS:")
        print(f"   🎬 Videos created: {self.stats['videos_created']}")
        print(f"   ⏱️ Total duration: {self.stats['total_duration']}s")
        print(f"   📄 Slides generated: {self.stats['slides_generated']}")
        print(f"   🎵 Audio files: {self.stats['audio_files_created']}")
    
    def show_status(self):
        """Show system status and capabilities"""
        print("\n🔍 SYSTEM STATUS")
        print("=" * 30)
        
        if self.video_engine:
            status = self.video_engine.get_engine_status()
            print("🎬 VIDEO ENGINE:")
            print(f"   📹 Video Processing: {'✅' if status['video_processing'] else '❌'}")
            print(f"   📄 Slide Creation: {'✅' if status['slide_creation'] else '❌'}")
            print(f"   🤖 AI Services: {'✅' if status['ai_services'] else '❌'}")
            print(f"   ☁️ Azure AI: {'✅' if status['azure_ai'] else '❌'}")
            print(f"   🗣️ Azure Speech: {'✅' if status['azure_speech'] else '❌'}")
            
            print(f"\n🎨 SUPPORTED THEMES:")
            for theme in status['supported_themes']:
                print(f"   • {theme}")
        else:
            print("❌ Video Engine not available")
        
        print(f"\n🗣️ VOICE SERVICES:")
        print(f"   Speech Synthesis: {'✅' if self.speech_service else '❌'}")
        
        session_duration = datetime.now() - self.stats['session_start']
        print(f"\n⏱️ SESSION INFO:")
        print(f"   Duration: {session_duration}")
        print(f"   Videos created: {self.stats['videos_created']}")
    
    def show_help(self):
        """Show comprehensive help"""
        print("\n❓ RUDH VIDEO ASSISTANT HELP")
        print("=" * 40)
        
        print("\n🎬 VIDEO CREATION COMMANDS:")
        print("   create video [topic] - Create explainer video")
        print("   create presentation [topic] - Business presentation")
        print("   create tutorial [topic] - Step-by-step tutorial")
        print("   create social [topic] - Social media video")
        print("   create pitch [topic] - Business pitch video")
        
        print("\n📋 NATURAL LANGUAGE EXAMPLES:")
        print("   'Create a video about AI portfolio management'")
        print("   'Make a presentation on Chennai tech market'")
        print("   'Generate tutorial for investment strategies'")
        print("   'Create social media content about fintech'")
        
        print("\n🛠️ UTILITY COMMANDS:")
        print("   templates - Show available video templates")
        print("   gallery - View created videos")
        print("   /status - System status and capabilities")
        print("   /help - Show this help")
        print("   /quit - Exit assistant")
        
        print("\n🎯 FEATURES:")
        print("   ✅ AI-powered script generation")
        print("   ✅ Professional slide creation")
        print("   ✅ Voice narration in Indian English")
        print("   ✅ Chennai business context integration")
        print("   ✅ Multiple themes (tech, finance, healthcare)")
        print("   ✅ Various video formats and durations")
    
    def parse_video_request(self, user_input: str) -> dict:
        """Parse natural language video creation requests"""
        input_lower = user_input.lower().strip()
        
        # Determine video type
        video_type = "explainer"  # default
        if any(word in input_lower for word in ['presentation', 'present', 'slides']):
            video_type = "presentation"
        elif any(word in input_lower for word in ['tutorial', 'how to', 'guide', 'steps']):
            video_type = "tutorial"
        elif any(word in input_lower for word in ['social', 'instagram', 'linkedin', 'short']):
            video_type = "social"
        elif any(word in input_lower for word in ['pitch', 'proposal', 'convince', 'sell']):
            video_type = "pitch"
        
        # Determine theme
        theme = "tech"  # default
        if any(word in input_lower for word in ['finance', 'investment', 'money', 'portfolio', 'stock']):
            theme = "finance"
        elif any(word in input_lower for word in ['health', 'medical', 'wellness', 'care']):
            theme = "healthcare"
        
        # Extract topic
        topic = user_input
        # Remove command words to get cleaner topic
        for phrase in ['create video about', 'create video', 'make video', 'make presentation', 'create presentation', 'generate', 'create']:
            topic = topic.replace(phrase, '').strip()
        
        if not topic:
            topic = "Business Intelligence"
        
        return {
            'topic': topic,
            'video_type': video_type,
            'theme': theme
        }
    
    def run(self):
        """Main interactive loop"""
        print("\n💬 Type your video creation request or command:")
        print("   Example: 'Create a video about AI portfolio management'")
        print("   Type '/help' for full command list")
        
        while True:
            try:
                print(f"\n[🎬] Your request: ", end="")
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['/quit', 'quit', 'exit']:
                    print("\n👋 Thank you for using Rudh Video Assistant!")
                    self.provide_voice_feedback("Thank you for using Rudh Video Assistant. Great videos await!")
                    break
                elif user_input.lower() in ['/help', 'help']:
                    self.show_help()
                elif user_input.lower() in ['/status', 'status']:
                    self.show_status()
                elif user_input.lower() in ['templates', 'show templates']:
                    self.show_templates()
                elif user_input.lower() in ['gallery', 'show gallery']:
                    self.show_gallery()
                
                # Handle video creation requests
                elif any(word in user_input.lower() for word in ['create', 'make', 'generate', 'video', 'presentation']):
                    request = self.parse_video_request(user_input)
                    
                    print(f"\n🎯 PARSED REQUEST:")
                    print(f"   📝 Topic: {request['topic']}")
                    print(f"   🎬 Type: {request['video_type']}")
                    print(f"   🎨 Theme: {request['theme']}")
                    
                    # Confirm with user
                    print(f"\n❓ Create {request['video_type']} video about '{request['topic']}'? (y/n): ", end="")
                    confirm = input().strip().lower()
                    
                    if confirm in ['y', 'yes', '']:
                        result = self.create_video(
                            request['topic'], 
                            request['video_type'], 
                            theme=request['theme']
                        )
                        
                        if result and result != "simulation_complete":
                            print(f"\n✅ Video created successfully!")
                            print(f"📁 File: {result}")
                        
                    else:
                        print("❌ Video creation cancelled")
                
                else:
                    print("❓ I didn't understand that request.")
                    print("💡 Try: 'Create a video about [your topic]' or type '/help'")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("💡 Type '/help' for assistance")

def main():
    """Launch Rudh Video Assistant"""
    try:
        assistant = RudhVideoAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Failed to start Video Assistant: {e}")
        print("💡 Try installing required dependencies or check system status")

if __name__ == "__main__":
    main()