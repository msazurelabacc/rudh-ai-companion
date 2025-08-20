# test_moviepy_integration.py
"""
Test MoviePy Integration for Enhanced Video Features
Verifies that all MoviePy components are working correctly
"""

import sys
import os
import time
from pathlib import Path

def test_moviepy_imports():
    """Test MoviePy imports and functionality"""
    print("🎬 Testing MoviePy Integration")
    print("=" * 40)
    
    try:
        # Test core MoviePy imports
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip,
            CompositeAudioClip, concatenate_videoclips, ImageSequenceClip
        )
        print("✅ Core MoviePy imports: SUCCESS")
        
        # Test video effects
        from moviepy.video.fx import resize, fadein, fadeout
        print("✅ Video effects imports: SUCCESS")
        
        # Test audio effects
        from moviepy.audio.fx import volumex
        print("✅ Audio effects imports: SUCCESS")
        
        return True
        
    except ImportError as e:
        print(f"❌ MoviePy import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ MoviePy test failed: {e}")
        return False

def test_basic_video_creation():
    """Test basic video creation with MoviePy"""
    print("\n🎥 Testing Basic Video Creation")
    print("=" * 35)
    
    try:
        from moviepy.editor import ImageClip, concatenate_videoclips
        import numpy as np
        from PIL import Image
        
        # Create test directory
        test_dir = Path("moviepy_test")
        test_dir.mkdir(exist_ok=True)
        
        # Create a simple test image
        print("📄 Creating test image...")
        img = Image.new('RGB', (1920, 1080), color='blue')
        img_path = test_dir / "test_slide.png"
        img.save(img_path)
        
        # Create video clip from image
        print("🎬 Creating video clip...")
        clip = ImageClip(str(img_path), duration=3.0)
        clip = clip.set_fps(24)
        
        # Apply fade effects
        print("✨ Applying fade effects...")
        from moviepy.video.fx import fadein, fadeout
        clip = fadein(clip, 0.5)
        clip = fadeout(clip, 0.5)
        
        # Export test video
        output_path = test_dir / "test_video.mp4"
        print(f"💾 Exporting test video: {output_path.name}")
        
        clip.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            verbose=False,
            logger=None
        )
        
        # Clean up
        clip.close()
        
        # Check result
        if output_path.exists():
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ Test video created successfully!")
            print(f"📊 File size: {file_size:.1f}KB")
            print(f"📁 Location: {output_path}")
            return True
        else:
            print("❌ Test video creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Video creation test failed: {e}")
        return False

def test_enhanced_video_engine():
    """Test the enhanced video engine with MoviePy"""
    print("\n🚀 Testing Enhanced Video Engine with MoviePy")
    print("=" * 50)
    
    try:
        # Import fixed enhanced engine
        from advanced_video_engine_v43_fixed import AdvancedVideoEngine
        
        print("📋 Initializing Enhanced Video Engine...")
        engine = AdvancedVideoEngine()
        
        # Check status
        status = engine.get_enhanced_status()
        print(f"🎬 Advanced Video Available: {status.get('advanced_video', False)}")
        
        if status.get('advanced_video', False):
            print("✅ MoviePy integration successful!")
            
            # Test enhanced video creation
            print("\n🎥 Testing Enhanced Video Creation...")
            
            test_script = {
                "title": "MoviePy Integration Test",
                "total_duration": 120,
                "scenes": [
                    {
                        "slide_text": "MoviePy Integration Success",
                        "narration": "Testing advanced video features with professional transitions and effects.",
                        "duration": 30
                    },
                    {
                        "slide_text": "Professional Video Production",
                        "narration": "Creating enterprise-grade videos with fade transitions and optimized timing.",
                        "duration": 30
                    },
                    {
                        "slide_text": "Chennai Business Excellence",
                        "narration": "Delivering professional content creation for Tamil Nadu business market.",
                        "duration": 30
                    },
                    {
                        "slide_text": "Enhanced Features Operational",
                        "narration": "Advanced video composition with MoviePy integration now fully functional.",
                        "duration": 30
                    }
                ]
            }
            
            start_time = time.time()
            result = engine.create_enhanced_video(test_script, "tech", "professional", "high")
            duration = time.time() - start_time
            
            if result:
                file_size = os.path.getsize(result) / (1024 * 1024) if os.path.exists(result) else 0
                print(f"✅ Enhanced video with MoviePy created!")
                print(f"📊 Size: {file_size:.1f}MB")
                print(f"⏱️ Creation time: {duration:.1f}s")
                print(f"📁 Location: {result}")
                return True
            else:
                print("❌ Enhanced video creation failed")
                return False
        else:
            print("⚠️ MoviePy not detected by engine")
            return False
            
    except ImportError as e:
        print(f"❌ Enhanced engine import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Enhanced engine test failed: {e}")
        return False

def main():
    """Run comprehensive MoviePy integration tests"""
    print("🎬 MOVIEPY INTEGRATION TEST SUITE")
    print("=" * 45)
    print("Testing advanced video features for Enhanced Video Assistant V4.3")
    
    results = []
    
    # Test 1: MoviePy imports
    results.append(test_moviepy_imports())
    
    # Test 2: Basic video creation
    results.append(test_basic_video_creation())
    
    # Test 3: Enhanced video engine
    results.append(test_enhanced_video_engine())
    
    # Summary
    print("\n🎯 TEST SUMMARY")
    print("=" * 20)
    print(f"✅ Tests passed: {sum(results)}/3")
    print(f"❌ Tests failed: {3 - sum(results)}/3")
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED!")
        print("🌟 Enhanced Video Features with MoviePy are FULLY OPERATIONAL!")
        print("\n🚀 READY FOR:")
        print("   ✅ Professional video transitions and fade effects")
        print("   ✅ Advanced slide timing and pacing control")
        print("   ✅ Multiple export quality options")
        print("   ✅ Enhanced video composition capabilities")
        print("   ✅ Complete professional video production pipeline")
    else:
        print("\n⚠️ Some tests failed. Check error messages above.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    if success:
        print("\n💡 Next step: Run enhanced video assistant for full features!")
        print("   Command: python rudh_enhanced_video_assistant_v43_fixed.py")
    else:
        print("\n💡 Check MoviePy installation and try again.")