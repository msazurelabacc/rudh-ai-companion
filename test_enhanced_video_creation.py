# test_enhanced_video_creation.py
"""
Enhanced Test Script for Rudh Video Creation V4.3
Tests advanced video production capabilities
"""

import sys
import os
import time

# Add current directory to path
sys.path.append('.')

def test_enhanced_engine():
    """Test enhanced video engine functionality"""
    print("🧪 Testing Enhanced Video Engine V4.3")
    print("=" * 50)
    
    try:
        from advanced_video_engine_v43 import AdvancedVideoEngine
        
        # Test 1: Enhanced engine initialization
        print("\n📊 Test 1: Enhanced Engine Initialization")
        engine = AdvancedVideoEngine()
        status = engine.get_enhanced_status()
        
        key_features = ['base_engine', 'advanced_video', 'audio_processing', 'speech_services']
        for feature in key_features:
            if feature in status:
                icon = "✅" if status[feature] else "❌"
                print(f"   {icon} {feature}: {status[feature]}")
        
        # Test 2: Enhanced script generation
        print("\n📝 Test 2: Enhanced Script Generation")
        
        # Create test script for enhanced video
        test_script = {
            "title": "Enhanced AI Portfolio Management",
            "total_duration": 180,
            "scenes": [
                {
                    "slide_text": "AI Portfolio Revolution",
                    "narration": "Welcome to the revolutionary world of AI-powered portfolio management, transforming how Chennai investors approach wealth building.",
                    "duration": 45
                },
                {
                    "slide_text": "Smart Investment Strategies",
                    "narration": "Discover advanced algorithms that analyze market patterns, optimize risk-return ratios, and deliver superior investment outcomes.",
                    "duration": 45
                },
                {
                    "slide_text": "Chennai Market Advantage",
                    "narration": "Leverage unique opportunities in Tamil Nadu's growing financial sector with AI-driven insights tailored for local market conditions.",
                    "duration": 45
                },
                {
                    "slide_text": "Your Investment Future",
                    "narration": "Transform your investment approach today with cutting-edge AI technology and start building wealth like never before.",
                    "duration": 45
                }
            ]
        }
        
        print(f"   ✅ Enhanced script: {test_script['title']}")
        print(f"   📊 Enhanced scenes: {len(test_script['scenes'])}")
        print(f"   🎭 Narration included: Yes")
        
        # Test 3: Enhanced video creation
        print("\n🎬 Test 3: Enhanced Video Creation")
        start_time = time.time()
        
        result = engine.create_enhanced_video(test_script, "finance", "professional", "high")
        
        creation_time = time.time() - start_time
        
        if result:
            file_size = os.path.getsize(result) / (1024 * 1024) if os.path.exists(result) else 0
            print(f"   ✅ Enhanced video created: {os.path.basename(result)}")
            print(f"   📊 Size: {file_size:.1f}MB")
            print(f"   ⏱️ Creation time: {creation_time:.1f}s")
            print(f"   🎯 Type: Enhanced professional video")
        else:
            print("   ❌ Enhanced video creation failed")
        
        print("\n🎯 Enhanced Testing Complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure advanced_video_engine_v43.py is in the current directory")
        print("💡 Install required dependencies: moviepy, scipy")
    except Exception as e:
        print(f"❌ Enhanced test error: {e}")

def test_enhanced_assistant():
    """Test enhanced video assistant"""
    print("\n🎬 Testing Enhanced Video Assistant")
    print("=" * 45)
    
    try:
        from rudh_enhanced_video_assistant_v43 import RudhEnhancedVideoAssistant
        
        print("✅ Enhanced Video Assistant imported successfully")
        assistant = RudhEnhancedVideoAssistant()
        
        print("✅ Enhanced Assistant initialized")
        print("💡 To test interactively, run: python rudh_enhanced_video_assistant_v43.py")
        
        # Test enhanced features
        print("\n🌟 Enhanced Features Available:")
        if hasattr(assistant, 'enhanced_templates'):
            print(f"   📋 Enhanced Templates: {len(assistant.enhanced_templates)}")
        if hasattr(assistant, 'quality_presets'):
            print(f"   💎 Quality Presets: {len(assistant.quality_presets)}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Enhanced assistant test error: {e}")

def test_dependencies():
    """Test all enhanced dependencies"""
    print("\n📦 Testing Enhanced Dependencies")
    print("=" * 40)
    
    dependencies = {
        'moviepy': 'Advanced video editing',
        'scipy': 'Audio processing',
        'numpy': 'Numerical computing',
        'cv2': 'Computer vision',
        'PIL': 'Image processing',
        'matplotlib': 'Plotting and visualization'
    }
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ❌ {package}: {description} - NOT INSTALLED")

if __name__ == "__main__":
    test_dependencies()
    test_enhanced_engine() 
    test_enhanced_assistant()
