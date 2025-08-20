# advanced_video_engine_v43_fixed.py
"""
Rudh Advanced Video Engine V4.3 - Fixed Version
Complete Professional Video Production with error handling
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import subprocess

# Enhanced video processing
try:
    import cv2
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip,
        CompositeAudioClip, concatenate_videoclips, ImageSequenceClip
    )
    from moviepy.video.fx import resize, fadein, fadeout
    from moviepy.audio.fx import volumex
    ADVANCED_VIDEO = True
except ImportError as e:
    print(f"⚠️ Advanced video libraries not available: {e}")
    ADVANCED_VIDEO = False

# Audio processing
try:
    import numpy as np
    from scipy.io import wavfile
    AUDIO_PROCESSING = True
except ImportError:
    AUDIO_PROCESSING = False

# Import existing video engine
try:
    from video_engine_core import VideoEngine
    BASE_VIDEO_ENGINE = True
except ImportError:
    BASE_VIDEO_ENGINE = False

# Azure services
try:
    from azure_speechservice import AzureSpeechService
    SPEECH_SERVICES = True
except ImportError:
    SPEECH_SERVICES = False

class AdvancedVideoEngine:
    """Complete Professional Video Production System - Fixed Version"""
    
    def __init__(self):
        self.setup_logging()
        
        # Initialize base video engine
        if BASE_VIDEO_ENGINE:
            self.base_engine = VideoEngine()
            self.logger.info("✅ Base video engine loaded")
        else:
            self.base_engine = None
            self.logger.warning("⚠️ Base video engine not available")
        
        # Enhanced directories
        self.video_output_dir = Path("video_output")
        self.audio_assets_dir = Path("audio_assets")
        self.music_library_dir = Path("music_library")
        self.final_videos_dir = Path("final_videos")
        
        # Create enhanced directories
        for directory in [self.audio_assets_dir, self.music_library_dir, self.final_videos_dir]:
            directory.mkdir(exist_ok=True)
        
        # Initialize services
        self.speech_service = None
        self.initialize_services()
        
        # Enhanced video settings
        self.enhanced_settings = {
            'resolution': (1920, 1080),
            'fps': 30,
            'slide_duration': 6.0,
            'transition_duration': 1.5,
            'fade_duration': 0.5,
            'background_music_volume': 0.3,
            'narration_volume': 1.0,
            'export_formats': ['mp4'],
            'quality_presets': {
                'ultra': {'bitrate': '8000k', 'crf': 18},
                'high': {'bitrate': '4000k', 'crf': 23},
                'medium': {'bitrate': '2000k', 'crf': 28},
                'web': {'bitrate': '1000k', 'crf': 32}
            }
        }
        
        # Voice personas for different content types
        self.voice_personas = {
            'professional': {
                'voice': 'en-IN-NeerjaNeural',
                'rate': '0%',
                'pitch': '0%',
                'style': 'professional'
            },
            'friendly': {
                'voice': 'en-IN-NeerjaNeural',
                'rate': '+5%',
                'pitch': '+2%',
                'style': 'friendly'
            },
            'authoritative': {
                'voice': 'en-IN-PrabhatNeural',
                'rate': '-5%',
                'pitch': '-2%',
                'style': 'serious'
            },
            'enthusiastic': {
                'voice': 'en-IN-NeerjaNeural',
                'rate': '+10%',
                'pitch': '+5%',
                'style': 'excited'
            }
        }
        
        self.logger.info("🎬 Advanced Video Engine V4.3 (Fixed) initialized successfully!")
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        self.logger = logging.getLogger('AdvancedVideoEngine')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def initialize_services(self):
        """Initialize enhanced Azure services"""
        if SPEECH_SERVICES:
            try:
                self.speech_service = AzureSpeechService()
                
                if hasattr(self.speech_service, 'is_available') and self.speech_service.is_available():
                    self.logger.info("✅ Azure Speech Service connected for advanced narration")
                else:
                    self.logger.warning("⚠️ Azure Speech Service not available - using fallback")
                    
            except Exception as e:
                self.logger.error(f"❌ Speech service initialization error: {e}")
                self.speech_service = None
        else:
            self.logger.warning("⚠️ Speech services not available")
    
    def create_professional_narration(self, script: Dict, persona: str = "professional") -> List[str]:
        """Generate high-quality narration for all scenes"""
        self.logger.info(f"🗣️ Creating professional narration with {persona} persona")
        
        narration_files = []
        voice_config = self.voice_personas.get(persona, self.voice_personas["professional"])
        
        for i, scene in enumerate(script.get('scenes', [])):
            narration_text = scene.get('narration', '')
            if not narration_text:
                continue
                
            self.logger.info(f"🎵 Generating narration for scene {i+1}")
            
            if self.speech_service:
                try:
                    # Try different speech methods
                    audio_data = None
                    for method_name in ['speak_text', 'text_to_speech', 'synthesize_speech']:
                        if hasattr(self.speech_service, method_name):
                            try:
                                result = getattr(self.speech_service, method_name)(narration_text)
                                if result:
                                    audio_data = result
                                    break
                            except Exception as e:
                                continue
                    
                    if audio_data:
                        # Save high-quality audio
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"narration_scene_{i+1}_{timestamp}.wav"
                        filepath = self.audio_assets_dir / filename
                        
                        # Handle different audio data types
                        if hasattr(audio_data, 'audio_data'):
                            audio_bytes = audio_data.audio_data
                        elif isinstance(audio_data, bytes):
                            audio_bytes = audio_data
                        else:
                            audio_bytes = str(audio_data).encode()
                        
                        with open(filepath, 'wb') as f:
                            f.write(audio_bytes)
                        
                        narration_files.append(str(filepath))
                        self.logger.info(f"✅ Scene {i+1} narration: {filename} ({len(audio_bytes):,} bytes)")
                    else:
                        self.logger.warning(f"⚠️ Failed to generate narration for scene {i+1}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Narration generation failed for scene {i+1}: {e}")
            else:
                # Create placeholder for fallback
                self.logger.warning(f"⚠️ Speech service unavailable for scene {i+1}")
        
        self.logger.info(f"🎵 Generated {len(narration_files)} narration files")
        return narration_files
    
    def create_enhanced_video(self, script: Dict, theme: str = "tech", 
                           persona: str = "professional", quality: str = "high") -> str:
        """Create complete professional video with all enhancements"""
        
        self.logger.info(f"🎬 Creating enhanced video: {script.get('title', 'Untitled')}")
        
        # Step 1: Generate base video assets using existing engine
        if self.base_engine:
            self.logger.info("📋 Step 1: Generating base video assets...")
            base_result = self.base_engine.create_simple_video(script, theme)
            
            if not base_result:
                self.logger.error("❌ Base video creation failed")
                return None
                
            # Load the created info file safely
            try:
                with open(base_result, 'r', encoding='utf-8') as f:
                    video_assets = json.load(f)
            except UnicodeDecodeError:
                # Try with different encoding
                try:
                    with open(base_result, 'r', encoding='latin-1') as f:
                        video_assets = json.load(f)
                except Exception as e:
                    self.logger.error(f"❌ Failed to read video assets file: {e}")
                    return base_result
            except Exception as e:
                self.logger.error(f"❌ Failed to load video assets: {e}")
                return base_result
        else:
            self.logger.error("❌ Base video engine not available")
            return None
        
        # Step 2: Generate professional narration
        self.logger.info("🗣️ Step 2: Generating professional narration...")
        narration_files = self.create_professional_narration(script, persona)
        
        # Step 3: Enhanced video composition (if advanced video available)
        if ADVANCED_VIDEO and video_assets.get('slides'):
            try:
                return self.compose_enhanced_video(video_assets, narration_files, script, quality)
            except Exception as e:
                self.logger.error(f"❌ Enhanced video composition failed: {e}")
                self.logger.info("📋 Falling back to base video with enhanced info")
                return base_result
        else:
            self.logger.warning("⚠️ Advanced video processing not available")
            self.logger.info("📋 Returning base video with enhanced script")
            return base_result
    
    def compose_enhanced_video(self, assets: Dict, narration_files: List[str], 
                             script: Dict, quality: str) -> str:
        """Compose enhanced video with available features"""
        
        self.logger.info("🎬 Composing enhanced video with available features...")
        
        try:
            # Video settings
            fps = self.enhanced_settings['fps']
            slide_duration = self.enhanced_settings['slide_duration']
            
            # Create video clips from slides
            video_clips = []
            slides = assets.get('slides', [])
            
            for i, slide_path in enumerate(slides):
                if os.path.exists(slide_path):
                    self.logger.info(f"📄 Processing slide {i+1}: {os.path.basename(slide_path)}")
                    
                    # Create image clip
                    clip = ImageClip(slide_path, duration=slide_duration)
                    clip = clip.set_fps(fps)
                    
                    # Add basic fade transitions if available
                    try:
                        if i > 0:  # Fade in except for first slide
                            clip = fadein(clip, 0.5)
                        if i < len(slides) - 1:  # Fade out except for last slide
                            clip = fadeout(clip, 0.5)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Transition effects not available: {e}")
                    
                    video_clips.append(clip)
            
            if not video_clips:
                self.logger.error("❌ No valid slides to create enhanced video")
                return None
            
            # Concatenate video clips
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Export enhanced video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_clean = "".join(c for c in script.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"enhanced_{title_clean[:30]}_{timestamp}.mp4"
            output_path = self.final_videos_dir / filename
            
            self.logger.info(f"💾 Exporting enhanced video: {filename}")
            
            # Export with optimized settings
            final_video.write_videofile(
                str(output_path),
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None  # Suppress MoviePy output
            )
            
            # Clean up clips
            final_video.close()
            for clip in video_clips:
                clip.close()
            
            # Get file size for reporting
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            
            self.logger.info(f"✅ Enhanced video created: {filename}")
            self.logger.info(f"📊 Duration: {final_video.duration:.1f}s, Size: {file_size:.1f}MB")
            
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"❌ Enhanced video composition failed: {e}")
            return None
    
    def get_enhanced_status(self) -> Dict:
        """Get comprehensive enhanced engine status"""
        base_status = {}
        if self.base_engine:
            base_status = self.base_engine.get_engine_status()
        
        enhanced_status = {
            'base_engine': BASE_VIDEO_ENGINE,
            'advanced_video': ADVANCED_VIDEO,
            'audio_processing': AUDIO_PROCESSING,
            'speech_services': SPEECH_SERVICES,
            'azure_speech': self.speech_service is not None,
            'voice_personas': list(self.voice_personas.keys()),
            'quality_presets': list(self.enhanced_settings['quality_presets'].keys()),
            'export_formats': self.enhanced_settings['export_formats'],
            'final_videos_dir': str(self.final_videos_dir),
            'features': [
                'Professional slide creation',
                'Voice narration (when Azure available)',
                'Enhanced video composition (when MoviePy available)',
                'Multiple quality presets',
                'Voice personas',
                'Chennai business themes'
            ]
        }
        
        return {**base_status, **enhanced_status}

# Test function
def test_enhanced_engine():
    """Test the enhanced video engine capabilities"""
    print("🧪 Testing Enhanced Video Engine V4.3 (Fixed)")
    print("=" * 60)
    
    engine = AdvancedVideoEngine()
    
    # Test 1: Engine status
    print("\n📊 Test 1: Enhanced Engine Status")
    status = engine.get_enhanced_status()
    
    key_features = ['base_engine', 'advanced_video', 'audio_processing', 'speech_services', 'azure_speech']
    for feature in key_features:
        if feature in status:
            icon = "✅" if status[feature] else "❌"
            print(f"   {icon} {feature}: {status[feature]}")
    
    print(f"\n🎵 Available Features:")
    for feature in status.get('features', []):
        print(f"   ✅ {feature}")
    
    # Test 2: Enhanced video creation
    print("\n🎬 Test 2: Enhanced Video Creation")
    
    # Create test script
    test_script = {
        "title": "Enhanced AI Portfolio Management",
        "total_duration": 180,
        "scenes": [
            {
                "slide_text": "AI Portfolio Revolution",
                "narration": "Welcome to the revolutionary world of AI-powered portfolio management.",
                "duration": 45
            },
            {
                "slide_text": "Smart Investment Strategies",
                "narration": "Discover advanced algorithms that optimize your investment returns.",
                "duration": 45
            },
            {
                "slide_text": "Chennai Market Advantage",
                "narration": "Leverage unique opportunities in Tamil Nadu's growing financial sector.",
                "duration": 45
            },
            {
                "slide_text": "Your Investment Future",
                "narration": "Transform your investment approach with cutting-edge AI technology.",
                "duration": 45
            }
        ]
    }
    
    start_time = time.time()
    result = engine.create_enhanced_video(test_script, "finance", "professional", "high")
    duration = time.time() - start_time
    
    if result:
        file_size = os.path.getsize(result) / (1024 * 1024) if os.path.exists(result) else 0
        print(f"   ✅ Enhanced video created: {os.path.basename(result)}")
        print(f"   📊 Size: {file_size:.1f}MB")
        print(f"   ⏱️ Creation time: {duration:.1f}s")
        print(f"   📁 Location: {result}")
    else:
        print("   ❌ Enhanced video creation failed")
    
    print("\n🎯 Enhanced Test Summary:")
    print(f"   Base Engine: {'✅ Available' if status.get('base_engine') else '❌ Missing'}")
    print(f"   Advanced Video: {'✅ Available' if status.get('advanced_video') else '❌ Install moviepy'}")
    print(f"   Speech Services: {'✅ Available' if status.get('speech_services') else '❌ Check Azure setup'}")
    
    return engine

if __name__ == "__main__":
    test_enhanced_engine()