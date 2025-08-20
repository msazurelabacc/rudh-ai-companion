# advanced_video_engine_v43.py
"""
Rudh Advanced Video Engine V4.3 - Complete Professional Video Production
Adds voice narration, background music, transitions, and advanced features
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
except ImportError:
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
    """Complete Professional Video Production System"""
    
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
            'slide_duration': 6.0,  # Longer for narration
            'transition_duration': 1.5,
            'fade_duration': 0.5,
            'background_music_volume': 0.3,
            'narration_volume': 1.0,
            'export_formats': ['mp4', 'webm', 'mov'],
            'quality_presets': {
                'ultra': {'bitrate': '8000k', 'crf': 18},
                'high': {'bitrate': '4000k', 'crf': 23},
                'medium': {'bitrate': '2000k', 'crf': 28},
                'web': {'bitrate': '1000k', 'crf': 32}
            }
        }
        
        # Professional music tracks (metadata for royalty-free music)
        self.music_library = {
            'corporate': {
                'uplifting': 'corporate_uplifting.mp3',
                'professional': 'corporate_professional.mp3',
                'inspiring': 'corporate_inspiring.mp3'
            },
            'tech': {
                'modern': 'tech_modern.mp3',
                'innovation': 'tech_innovation.mp3',
                'digital': 'tech_digital.mp3'
            },
            'finance': {
                'success': 'finance_success.mp3',
                'growth': 'finance_growth.mp3',
                'stability': 'finance_stability.mp3'
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
        
        self.logger.info("🎬 Advanced Video Engine V4.3 initialized successfully!")
        
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
                    # Enhanced SSML for better voice control
                    ssml_text = f"""
                    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-IN">
                        <voice name="{voice_config['voice']}">
                            <prosody rate="{voice_config['rate']}" pitch="{voice_config['pitch']}">
                                {narration_text}
                            </prosody>
                        </voice>
                    </speak>
                    """
                    
                    # Try different speech methods
                    audio_data = None
                    for method_name in ['speak_text', 'text_to_speech', 'synthesize_speech']:
                        if hasattr(self.speech_service, method_name):
                            try:
                                result = getattr(self.speech_service, method_name)(ssml_text)
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
    
    def select_background_music(self, theme: str, mood: str = "professional") -> str:
        """Select appropriate background music"""
        music_category = self.music_library.get(theme, self.music_library["corporate"])
        music_file = music_category.get(mood, list(music_category.values())[0])
        
        music_path = self.music_library_dir / music_file
        
        # Create placeholder music file if not exists
        if not music_path.exists():
            self.create_placeholder_music(music_path)
        
        return str(music_path)
    
    def create_placeholder_music(self, filepath: Path):
        """Create placeholder background music for testing"""
        self.logger.info(f"🎵 Creating placeholder music: {filepath.name}")
        
        try:
            if AUDIO_PROCESSING:
                # Generate simple background tone
                duration = 300  # 5 minutes
                sample_rate = 44100
                
                # Create subtle background ambience
                t = np.linspace(0, duration, duration * sample_rate, False)
                frequency1 = 220  # A3
                frequency2 = 330  # E4
                
                # Create soft ambient tones
                wave1 = 0.1 * np.sin(2 * np.pi * frequency1 * t)
                wave2 = 0.05 * np.sin(2 * np.pi * frequency2 * t)
                ambient = wave1 + wave2
                
                # Add fade in/out
                fade_samples = sample_rate * 2  # 2 second fade
                ambient[:fade_samples] *= np.linspace(0, 1, fade_samples)
                ambient[-fade_samples:] *= np.linspace(1, 0, fade_samples)
                
                # Save as WAV
                wavfile.write(str(filepath), sample_rate, (ambient * 32767).astype(np.int16))
                self.logger.info(f"✅ Created ambient music: {filepath.name}")
            else:
                # Create empty file as placeholder
                filepath.touch()
                self.logger.info(f"✅ Created placeholder: {filepath.name}")
                
        except Exception as e:
            self.logger.error(f"❌ Music creation failed: {e}")
            # Create empty file as fallback
            filepath.touch()
    
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
                
            # Load the created info file
            with open(base_result, 'r', encoding='utf-8') as f:
                video_assets = json.load(f)
        else:
            self.logger.error("❌ Base video engine not available")
            return None
        
        # Step 2: Generate professional narration
        self.logger.info("🗣️ Step 2: Generating professional narration...")
        narration_files = self.create_professional_narration(script, persona)
        
        # Step 3: Select background music
        self.logger.info("🎵 Step 3: Selecting background music...")
        music_file = self.select_background_music(theme, "professional")
        
        # Step 4: Create enhanced video with MoviePy
        if ADVANCED_VIDEO and video_assets.get('slides'):
            try:
                return self.compose_final_video(video_assets, narration_files, music_file, script, quality)
            except Exception as e:
                self.logger.error(f"❌ Advanced video composition failed: {e}")
                return base_result
        else:
            self.logger.warning("⚠️ Advanced video processing not available")
            return base_result
    
    def compose_final_video(self, assets: Dict, narration_files: List[str], 
                          music_file: str, script: Dict, quality: str) -> str:
        """Compose final professional video with all elements"""
        
        self.logger.info("🎬 Composing final professional video...")
        
        try:
            # Video settings
            fps = self.enhanced_settings['fps']
            slide_duration = self.enhanced_settings['slide_duration']
            transition_duration = self.enhanced_settings['transition_duration']
            fade_duration = self.enhanced_settings['fade_duration']
            
            # Create video clips from slides
            video_clips = []
            slides = assets.get('slides', [])
            
            for i, slide_path in enumerate(slides):
                if os.path.exists(slide_path):
                    self.logger.info(f"📄 Processing slide {i+1}: {os.path.basename(slide_path)}")
                    
                    # Create image clip
                    clip = ImageClip(slide_path, duration=slide_duration)
                    clip = clip.set_fps(fps)
                    
                    # Add fade transitions
                    if i > 0:  # Fade in except for first slide
                        clip = fadein(clip, fade_duration)
                    if i < len(slides) - 1:  # Fade out except for last slide
                        clip = fadeout(clip, fade_duration)
                    
                    video_clips.append(clip)
            
            if not video_clips:
                self.logger.error("❌ No valid slides to create video")
                return None
            
            # Concatenate video clips
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Add narration audio if available
            if narration_files and os.path.exists(narration_files[0]):
                try:
                    self.logger.info("🗣️ Adding narration audio...")
                    
                    # Load and concatenate narration files
                    audio_clips = []
                    for narration_file in narration_files:
                        if os.path.exists(narration_file):
                            audio_clip = AudioFileClip(narration_file)
                            audio_clips.append(audio_clip)
                    
                    if audio_clips:
                        # Concatenate all narration
                        narration_audio = concatenate_audioclips(audio_clips)
                        
                        # Adjust video duration to match audio
                        if narration_audio.duration > final_video.duration:
                            final_video = final_video.set_duration(narration_audio.duration)
                        
                        # Set narration as main audio
                        final_video = final_video.set_audio(narration_audio)
                        self.logger.info(f"✅ Narration added ({narration_audio.duration:.1f}s)")
                        
                except Exception as e:
                    self.logger.warning(f"⚠️ Narration addition failed: {e}")
            
            # Add background music if available
            if os.path.exists(music_file) and os.path.getsize(music_file) > 0:
                try:
                    self.logger.info("🎵 Adding background music...")
                    
                    background_music = AudioFileClip(music_file)
                    background_music = background_music.set_duration(final_video.duration)
                    background_music = volumex(background_music, self.enhanced_settings['background_music_volume'])
                    
                    # Combine narration and background music
                    if final_video.audio:
                        combined_audio = CompositeAudioClip([final_video.audio, background_music])
                        final_video = final_video.set_audio(combined_audio)
                    else:
                        final_video = final_video.set_audio(background_music)
                    
                    self.logger.info("✅ Background music added")
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Background music addition failed: {e}")
            
            # Export final video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_clean = "".join(c for c in script.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"enhanced_{title_clean[:30]}_{timestamp}.mp4"
            output_path = self.final_videos_dir / filename
            
            # Quality settings
            quality_config = self.enhanced_settings['quality_presets'][quality]
            
            self.logger.info(f"💾 Exporting final video: {filename}")
            
            # Export with high quality settings
            final_video.write_videofile(
                str(output_path),
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                bitrate=quality_config['bitrate'],
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
            self.logger.error(f"❌ Video composition failed: {e}")
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
            'music_library': len(self.music_library),
            'voice_personas': list(self.voice_personas.keys()),
            'quality_presets': list(self.enhanced_settings['quality_presets'].keys()),
            'export_formats': self.enhanced_settings['export_formats'],
            'final_videos_dir': str(self.final_videos_dir),
            'features': [
                'Professional narration',
                'Background music',
                'Fade transitions',
                'Multiple quality presets',
                'Voice personas',
                'Chennai business themes'
            ]
        }
        
        return {**base_status, **enhanced_status}

# Test function
def test_advanced_engine():
    """Test the advanced video engine capabilities"""
    print("🧪 Testing Advanced Video Engine V4.3")
    print("=" * 55)
    
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
        "title": "AI Portfolio Management Mastery",
        "total_duration": 120,
        "scenes": [
            {
                "slide_text": "Welcome to AI Portfolio Management",
                "narration": "Welcome to the future of investment management. Today we'll explore how artificial intelligence is revolutionizing portfolio optimization.",
                "duration": 30
            },
            {
                "slide_text": "Key Benefits of AI Investment",
                "narration": "AI-powered portfolio management offers superior risk assessment, automated rebalancing, and data-driven decision making for better returns.",
                "duration": 30
            },
            {
                "slide_text": "Chennai Market Opportunities",
                "narration": "Chennai's growing financial sector provides unique opportunities for AI implementation, especially in regional investment strategies.",
                "duration": 30
            },
            {
                "slide_text": "Take Action Today",
                "narration": "Start your AI-powered investment journey today and experience the future of wealth management.",
                "duration": 30
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
    
    print("\n🎯 Test Summary:")
    print(f"   Advanced Video: {'✅ Available' if ADVANCED_VIDEO else '❌ Install moviepy'}")
    print(f"   Audio Processing: {'✅ Available' if AUDIO_PROCESSING else '❌ Install scipy'}")
    print(f"   Speech Services: {'✅ Available' if SPEECH_SERVICES else '❌ Check Azure setup'}")
    
    return engine

if __name__ == "__main__":
    test_advanced_engine()