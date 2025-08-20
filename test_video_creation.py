# test_video_creation.py
"""
Test script for Rudh Video Creation V4.2
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

def test_video_engine():
    """Test video engine functionality"""
    print("🧪 Testing Video Engine V4.2")
    print("=" * 40)
    
    try:
        from video_engine_core import VideoEngine
        
        # Test 1: Engine initialization
        print("\n📊 Test 1: Engine Initialization")
        engine = VideoEngine()
        status = engine.get_engine_status()
        
        for key, value in status.items():
            if key not in ['video_settings']:
                icon = "✅" if value else "❌"
                print(f"   {icon} {key}: {value}")
        
        # Test 2: Script generation
        print("\n📝 Test 2: Script Generation")
        script = engine.create_video_script("Portfolio Management", "explainer", 120)
        print(f"   ✅ Script: {script.get('title', 'Generated')}")
        print(f"   📊 Scenes: {len(script.get('scenes', []))}")
        
        # Test 3: Video creation
        print("\n🎬 Test 3: Video Creation")
        result = engine.create_simple_video(script, "finance")
        
        if result:
            print(f"   ✅ Created: {os.path.basename(result)}")
        else:
            print("   ❌ Creation failed")
        
        print("\n🎯 Testing complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure video_engine_core.py is in the current directory")
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_video_assistant():
    """Test interactive video assistant"""
    print("\n🎬 Testing Video Assistant")
    print("=" * 35)
    
    try:
        from rudh_video_assistant_v42 import RudhVideoAssistant
        
        print("✅ Video Assistant imported successfully")
        assistant = RudhVideoAssistant()
        
        print("✅ Assistant initialized")
        print("💡 To test interactively, run: python rudh_video_assistant_v42.py")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_video_engine()
    test_video_assistant()
