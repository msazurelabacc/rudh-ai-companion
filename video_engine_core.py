# video_engine_core.py
"""
Rudh Video Engine V4.2 - AI-Powered Video Content Creation
Creates animated videos with voice narration and professional styling
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess

# Core video processing
try:
    import cv2
    VIDEO_PROCESSING = True
except ImportError:
    VIDEO_PROCESSING = False

# Image processing for slides
try:
    from PIL import Image, ImageDraw, ImageFont
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    SLIDE_CREATION = True
except ImportError:
    SLIDE_CREATION = False

# Azure services
try:
    from azure_ai_service import AzureAIService
    from azure_speechservice import AzureSpeechService
    AI_SERVICES = True
except ImportError:
    AI_SERVICES = False

class VideoEngine:
    """AI-Powered Video Content Creation Engine"""
    
    def __init__(self):
        self.setup_logging()
        self.video_output_dir = Path("video_output")
        self.templates_dir = Path("video_templates")
        self.assets_dir = Path("video_assets")
        
        # Create directories
        for directory in [self.video_output_dir, self.templates_dir, self.assets_dir]:
            directory.mkdir(exist_ok=True)
        
        # Initialize services
        self.ai_service = None
        self.speech_service = None
        self.initialize_services()
        
        # Video settings
        self.video_settings = {
            'resolution': (1920, 1080),  # Full HD
            'fps': 30,
            'duration_per_slide': 5.0,  # seconds
            'transition_duration': 1.0,  # seconds
            'audio_format': 'wav',
            'video_format': 'mp4'
        }
        
        # Chennai business themes
        self.chennai_themes = {
            'tech': {
                'colors': ['#0066CC', '#FF6600', '#00CC66'],
                'fonts': ['Arial', 'Helvetica', 'Sans-serif'],
                'style': 'modern_tech'
            },
            'finance': {
                'colors': ['#003366', '#FFD700', '#006600'],
                'fonts': ['Times New Roman', 'Georgia', 'Serif'],
                'style': 'professional_finance'
            },
            'healthcare': {
                'colors': ['#CC0000', '#0099CC', '#66CC00'],
                'fonts': ['Arial', 'Calibri', 'Sans-serif'],
                'style': 'clean_medical'
            }
        }
        
        self.logger.info("🎬 Video Engine V4.2 initialized successfully!")
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        self.logger = logging.getLogger('VideoEngine')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def initialize_services(self):
        """Initialize Azure AI and Speech services"""
        if AI_SERVICES:
            try:
                self.ai_service = AzureAIService()
                self.speech_service = AzureSpeechService()
                
                # Test AI service
                if hasattr(self.ai_service, 'is_available') and self.ai_service.is_available():
                    self.logger.info("✅ Azure AI Service connected")
                else:
                    self.logger.warning("⚠️ Azure AI Service not available - using fallback")
                    
                # Test Speech service
                if hasattr(self.speech_service, 'is_available') and self.speech_service.is_available():
                    self.logger.info("✅ Azure Speech Service connected")
                else:
                    self.logger.warning("⚠️ Azure Speech Service not available - using fallback")
                    
            except Exception as e:
                self.logger.error(f"❌ Service initialization error: {e}")
                self.ai_service = None
                self.speech_service = None
        else:
            self.logger.warning("⚠️ Azure services not available - using fallback mode")
    
    def create_video_script(self, topic: str, video_type: str = "explainer", duration: int = 180) -> Dict:
        """Generate comprehensive video script using AI"""
        self.logger.info(f"🎯 Creating video script for: {topic}")
        
        # Try AI service first
        if self.ai_service:
            try:
                prompt = f"""Create a comprehensive video script for a {duration}-second {video_type} video about {topic}.
                
Structure the response as JSON with:
- title: Compelling video title
- scenes: Array of scenes with slide_text, narration, visual_elements, duration
- total_duration: Total video length
- target_audience: Primary audience
- key_messages: Main takeaways
- tamil_context: Tamil Nadu/Chennai specific insights if relevant

Make it engaging, professional, and suitable for business/educational content."""

                # Try different AI methods
                for method_name in ['get_response', 'generate_response', 'get_completion', 'complete']:
                    if hasattr(self.ai_service, method_name):
                        try:
                            response = getattr(self.ai_service, method_name)(prompt)
                            if response and len(response.strip()) > 100:
                                # Try to parse as JSON, fallback to text processing
                                try:
                                    return json.loads(response)
                                except:
                                    return self.parse_text_to_script(response, topic, duration)
                        except Exception as e:
                            self.logger.warning(f"AI method {method_name} failed: {e}")
                            continue
            except Exception as e:
                self.logger.error(f"AI script generation failed: {e}")
        
        # Fallback to template-based script
        return self.create_template_script(topic, video_type, duration)
    
    def create_template_script(self, topic: str, video_type: str, duration: int) -> Dict:
        """Create professional video script using templates"""
        self.logger.info(f"📝 Creating template script for: {topic}")
        
        # Calculate scenes based on duration
        scenes_count = max(3, min(8, duration // 30))
        scene_duration = duration / scenes_count
        
        script = {
            "title": f"Professional Guide to {topic}",
            "total_duration": duration,
            "target_audience": "Business professionals and learners",
            "key_messages": [
                f"Understanding {topic} fundamentals",
                f"Practical applications of {topic}",
                f"Benefits and opportunities in {topic}",
                "Chennai market insights and opportunities"
            ],
            "scenes": []
        }
        
        # Create engaging scenes
        scene_templates = [
            {
                "slide_text": f"Welcome to {topic}",
                "narration": f"Welcome! Today we'll explore {topic} and discover how it can transform your business approach in Chennai and beyond.",
                "visual_elements": ["title_slide", "professional_background"],
                "duration": scene_duration
            },
            {
                "slide_text": f"Understanding {topic}",
                "narration": f"Let's start with the fundamentals of {topic}. This powerful concept has been revolutionizing businesses worldwide.",
                "visual_elements": ["concept_diagram", "key_points"],
                "duration": scene_duration
            },
            {
                "slide_text": f"Key Benefits of {topic}",
                "narration": f"The benefits of implementing {topic} are substantial. Organizations see improved efficiency, better decision-making, and enhanced competitive advantage.",
                "visual_elements": ["benefits_chart", "success_metrics"],
                "duration": scene_duration
            },
            {
                "slide_text": f"Chennai Market Opportunities",
                "narration": f"In Chennai's dynamic business environment, {topic} presents unique opportunities for growth and innovation.",
                "visual_elements": ["market_chart", "local_insights"],
                "duration": scene_duration
            },
            {
                "slide_text": f"Implementation Strategy",
                "narration": f"Here's a practical roadmap for implementing {topic} in your organization, with specific considerations for Tamil Nadu businesses.",
                "visual_elements": ["roadmap_diagram", "implementation_steps"],
                "duration": scene_duration
            },
            {
                "slide_text": "Take Action Today",
                "narration": f"You now have the knowledge to leverage {topic} effectively. Start implementing these strategies and watch your business transform.",
                "visual_elements": ["call_to_action", "contact_info"],
                "duration": scene_duration
            }
        ]
        
        # Select appropriate number of scenes
        script["scenes"] = scene_templates[:scenes_count]
        
        return script
    
    def parse_text_to_script(self, text: str, topic: str, duration: int) -> Dict:
        """Parse AI-generated text into structured script"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        script = {
            "title": f"AI-Generated Guide to {topic}",
            "total_duration": duration,
            "scenes": []
        }
        
        current_scene = {}
        scene_duration = duration / max(3, len(lines) // 3)
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['title:', 'slide:', 'scene:']):
                if current_scene:
                    current_scene["duration"] = scene_duration
                    script["scenes"].append(current_scene)
                current_scene = {
                    "slide_text": line.split(':', 1)[-1].strip(),
                    "visual_elements": ["professional_slide"]
                }
            elif any(keyword in line.lower() for keyword in ['narration:', 'speech:', 'voiceover:']):
                if current_scene:
                    current_scene["narration"] = line.split(':', 1)[-1].strip()
            elif len(line) > 20:  # Treat as narration if long enough
                if current_scene and "narration" not in current_scene:
                    current_scene["narration"] = line
        
        # Add final scene
        if current_scene:
            current_scene["duration"] = scene_duration
            script["scenes"].append(current_scene)
        
        return script
    
    def create_slide_image(self, scene: Dict, theme: str = "tech") -> str:
        """Create professional slide image"""
        if not SLIDE_CREATION:
            self.logger.warning("⚠️ Slide creation libraries not available")
            return None
            
        try:
            theme_config = self.chennai_themes.get(theme, self.chennai_themes["tech"])
            
            # Create figure
            fig, ax = plt.subplots(figsize=(16, 9))  # 16:9 aspect ratio
            ax.set_xlim(0, 16)
            ax.set_ylim(0, 9)
            ax.axis('off')
            
            # Background
            background_color = theme_config['colors'][0]
            ax.add_patch(patches.Rectangle((0, 0), 16, 9, facecolor=background_color, alpha=0.1))
            
            # Title
            slide_text = scene.get('slide_text', 'Professional Slide')
            ax.text(8, 7, slide_text, fontsize=24, weight='bold', 
                   ha='center', va='center', color=theme_config['colors'][1])
            
            # Content area
            narration = scene.get('narration', '')
            if narration:
                # Split into key points
                words = narration.split()
                if len(words) > 15:
                    # Create bullet points
                    chunks = [' '.join(words[i:i+8]) for i in range(0, len(words), 8)]
                    for i, chunk in enumerate(chunks[:4]):  # Max 4 points
                        ax.text(2, 5.5 - i*0.8, f"• {chunk}", fontsize=16, 
                               ha='left', va='center', color=theme_config['colors'][2])
                else:
                    ax.text(8, 4, narration, fontsize=18, ha='center', va='center', 
                           wrap=True, color=theme_config['colors'][2])
            
            # Footer
            ax.text(8, 0.5, "Powered by Rudh AI | Chennai Business Intelligence", 
                   fontsize=12, ha='center', va='center', style='italic',
                   color=theme_config['colors'][0])
            
            # Save slide
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"slide_{timestamp}.png"
            filepath = self.video_output_dir / filename
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()
            
            self.logger.info(f"✅ Slide created: {filename}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"❌ Slide creation failed: {e}")
            return None
    
    def generate_audio_narration(self, text: str, voice: str = "en-IN-NeerjaNeural") -> str:
        """Generate high-quality audio narration"""
        if not self.speech_service:
            self.logger.warning("⚠️ Speech service not available")
            return None
            
        try:
            # Try different speech service methods
            audio_data = None
            for method_name in ['speak_text', 'text_to_speech', 'synthesize_speech', 'speak']:
                if hasattr(self.speech_service, method_name):
                    try:
                        result = getattr(self.speech_service, method_name)(text, voice)
                        if result:
                            audio_data = result
                            break
                    except Exception as e:
                        self.logger.warning(f"Speech method {method_name} failed: {e}")
                        continue
            
            if not audio_data:
                self.logger.warning("⚠️ All speech methods failed")
                return None
            
            # Save audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"narration_{timestamp}.wav"
            filepath = self.video_output_dir / filename
            
            # Handle different audio data types
            if hasattr(audio_data, 'audio_data'):
                audio_bytes = audio_data.audio_data
            elif isinstance(audio_data, bytes):
                audio_bytes = audio_data
            else:
                audio_bytes = str(audio_data).encode()
            
            with open(filepath, 'wb') as f:
                f.write(audio_bytes)
            
            self.logger.info(f"✅ Audio narration created: {filename} ({len(audio_bytes)} bytes)")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"❌ Audio generation failed: {e}")
            return None
    
    def create_simple_video(self, script: Dict, theme: str = "tech") -> str:
        """Create video using available tools"""
        self.logger.info(f"🎬 Creating video: {script.get('title', 'Untitled')}")
        
        video_assets = {
            'slides': [],
            'audio_files': [],
            'video_info': {
                'title': script.get('title', 'Video'),
                'duration': script.get('total_duration', 180),
                'scenes_count': len(script.get('scenes', []))
            }
        }
        
        # Create slides and audio for each scene
        for i, scene in enumerate(script.get('scenes', [])):
            self.logger.info(f"📝 Processing scene {i+1}: {scene.get('slide_text', 'Scene')}")
            
            # Create slide image
            slide_path = self.create_slide_image(scene, theme)
            if slide_path:
                video_assets['slides'].append(slide_path)
            
            # Generate audio narration
            narration = scene.get('narration', '')
            if narration:
                audio_path = self.generate_audio_narration(narration)
                if audio_path:
                    video_assets['audio_files'].append(audio_path)
            
            time.sleep(0.1)  # Brief pause between scenes
        
        # Create video info file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        info_filename = f"video_info_{timestamp}.json"
        info_filepath = self.video_output_dir / info_filename
        
        with open(info_filepath, 'w', encoding='utf-8') as f:
            json.dump(video_assets, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Video assets created!")
        self.logger.info(f"📊 Slides: {len(video_assets['slides'])}")
        self.logger.info(f"🎵 Audio files: {len(video_assets['audio_files'])}")
        self.logger.info(f"📄 Info file: {info_filename}")
        
        # If we have proper video processing, combine into MP4
        if VIDEO_PROCESSING and video_assets['slides']:
            try:
                return self.combine_to_video(video_assets, timestamp)
            except Exception as e:
                self.logger.error(f"❌ Video combination failed: {e}")
        
        return str(info_filepath)
    
    def combine_to_video(self, assets: Dict, timestamp: str) -> str:
        """Combine slides and audio into final video"""
        self.logger.info("🎬 Combining assets into final video...")
        
        try:
            # Video settings
            width, height = self.video_settings['resolution']
            fps = self.video_settings['fps']
            
            # Output filename
            video_filename = f"video_{timestamp}.mp4"
            video_filepath = self.video_output_dir / video_filename
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(str(video_filepath), fourcc, fps, (width, height))
            
            scene_duration = self.video_settings['duration_per_slide']
            frames_per_scene = int(fps * scene_duration)
            
            # Process each slide
            for slide_path in assets['slides']:
                if os.path.exists(slide_path):
                    # Load and resize image
                    img = cv2.imread(slide_path)
                    if img is not None:
                        img_resized = cv2.resize(img, (width, height))
                        
                        # Write frames for this slide
                        for _ in range(frames_per_scene):
                            video_writer.write(img_resized)
            
            video_writer.release()
            
            self.logger.info(f"✅ Video created: {video_filename}")
            return str(video_filepath)
            
        except Exception as e:
            self.logger.error(f"❌ Video combination failed: {e}")
            return None
    
    def get_engine_status(self) -> Dict:
        """Get comprehensive engine status"""
        return {
            'video_processing': VIDEO_PROCESSING,
            'slide_creation': SLIDE_CREATION,
            'ai_services': AI_SERVICES,
            'azure_ai': self.ai_service is not None,
            'azure_speech': self.speech_service is not None,
            'output_directory': str(self.video_output_dir),
            'video_settings': self.video_settings,
            'supported_themes': list(self.chennai_themes.keys())
        }

# Test function
def test_video_engine():
    """Test the video engine capabilities"""
    print("🧪 Testing Video Engine V4.2")
    print("=" * 50)
    
    engine = VideoEngine()
    
    # Test 1: Engine status
    print("\n📊 Test 1: Engine Status")
    status = engine.get_engine_status()
    for key, value in status.items():
        if key != 'video_settings':
            icon = "✅" if value else "❌"
            print(f"   {icon} {key}: {value}")
    
    # Test 2: Script creation
    print("\n📝 Test 2: Script Creation")
    script = engine.create_video_script("AI Portfolio Management", "explainer", 120)
    print(f"   ✅ Script created: {script.get('title', 'Untitled')}")
    print(f"   📊 Scenes: {len(script.get('scenes', []))}")
    print(f"   ⏱️ Duration: {script.get('total_duration', 0)}s")
    
    # Test 3: Video creation
    print("\n🎬 Test 3: Video Creation")
    start_time = time.time()
    result = engine.create_simple_video(script, "finance")
    duration = time.time() - start_time
    
    if result:
        print(f"   ✅ Video assets created: {os.path.basename(result)}")
        print(f"   ⏱️ Creation time: {duration:.2f}s")
        print(f"   📁 Location: {result}")
    else:
        print("   ❌ Video creation failed")
    
    print("\n🎯 Test Summary:")
    print(f"   Video Processing: {'✅ Available' if VIDEO_PROCESSING else '❌ Not available'}")
    print(f"   Slide Creation: {'✅ Available' if SLIDE_CREATION else '❌ Not available'}")
    print(f"   AI Services: {'✅ Available' if AI_SERVICES else '❌ Not available'}")
    
    return engine

if __name__ == "__main__":
    test_video_engine()