# setup_video_phase42.py
"""
Phase 4.2 Video Creation Setup Script
Sets up the complete video creation environment with dependencies and templates
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories for video creation"""
    print("📁 Creating video directories...")
    
    directories = [
        "video_output",
        "video_templates", 
        "video_assets",
        "video_cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created: {directory}/")

def install_video_dependencies():
    """Install video processing dependencies"""
    print("\n📦 Installing video processing dependencies...")
    
    # Core video dependencies
    video_packages = [
        "opencv-python",      # Video processing
        "Pillow",            # Image processing  
        "matplotlib",        # Chart/slide creation
        "numpy",             # Numerical processing
    ]
    
    # Optional advanced packages
    optional_packages = [
        "moviepy",           # Advanced video editing
        "imageio",           # Additional image formats
        "imageio-ffmpeg",    # FFmpeg wrapper
    ]
    
    print("🔧 Installing core video packages...")
    for package in video_packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ {package} failed: {e}")
    
    print("\n🎬 Installing optional video packages...")
    for package in optional_packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ {package} failed (optional): {e}")

def create_video_templates():
    """Create professional video templates"""
    print("\n📝 Creating video templates...")
    
    templates = {
        "business_explainer.json": {
            "name": "Business Explainer",
            "description": "Professional business concept explanation",
            "duration": 180,
            "scenes": [
                {
                    "type": "title",
                    "duration": 10,
                    "template": "Welcome to {topic} - Your Complete Guide"
                },
                {
                    "type": "introduction", 
                    "duration": 30,
                    "template": "Understanding {topic} fundamentals and key benefits"
                },
                {
                    "type": "main_content",
                    "duration": 120,
                    "template": "Deep dive into {topic} with practical examples"
                },
                {
                    "type": "conclusion",
                    "duration": 20,
                    "template": "Key takeaways and next steps for {topic}"
                }
            ]
        },
        
        "chennai_business.json": {
            "name": "Chennai Business Focus",
            "description": "Business content with Tamil Nadu context",
            "duration": 240,
            "local_elements": [
                "Tamil Nadu market insights",
                "Chennai business ecosystem",
                "Regional investment opportunities",
                "Local success stories"
            ]
        },
        
        "tech_tutorial.json": {
            "name": "Technical Tutorial", 
            "description": "Step-by-step technical instruction",
            "duration": 420,
            "structure": "problem -> solution -> implementation -> results"
        },
        
        "investment_analysis.json": {
            "name": "Investment Analysis",
            "description": "Financial analysis and recommendations", 
            "duration": 300,
            "sections": [
                "Market overview",
                "Risk assessment", 
                "Opportunity analysis",
                "Recommendations"
            ]
        }
    }
    
    templates_dir = Path("video_templates")
    
    for filename, template in templates.items():
        filepath = templates_dir / filename
        
        # Create JSON template file
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created template: {filename}")

def create_sample_assets():
    """Create sample video assets and resources"""
    print("\n🎨 Creating sample assets...")
    
    assets_dir = Path("video_assets")
    
    # Create sample color schemes
    color_schemes = {
        "chennai_tech.json": {
            "name": "Chennai Tech",
            "primary": "#0066CC",
            "secondary": "#FF6600", 
            "accent": "#00CC66",
            "background": "#FFFFFF",
            "text": "#333333"
        },
        
        "tamil_finance.json": {
            "name": "Tamil Finance",
            "primary": "#003366",
            "secondary": "#FFD700",
            "accent": "#006600", 
            "background": "#F8F9FA",
            "text": "#2C3E50"
        },
        
        "healthcare_professional.json": {
            "name": "Healthcare Professional",
            "primary": "#CC0000",
            "secondary": "#0099CC",
            "accent": "#66CC00",
            "background": "#FFFFFF", 
            "text": "#34495E"
        }
    }
    
    for filename, scheme in color_schemes.items():
        filepath = assets_dir / filename
        
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scheme, f, indent=2)
        
        print(f"✅ Created color scheme: {filename}")

def create_test_script():
    """Create test script for video creation"""
    print("\n🧪 Creating test script...")
    
    test_script = '''# test_video_creation.py
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
        print("\\n📊 Test 1: Engine Initialization")
        engine = VideoEngine()
        status = engine.get_engine_status()
        
        for key, value in status.items():
            if key not in ['video_settings']:
                icon = "✅" if value else "❌"
                print(f"   {icon} {key}: {value}")
        
        # Test 2: Script generation
        print("\\n📝 Test 2: Script Generation")
        script = engine.create_video_script("Portfolio Management", "explainer", 120)
        print(f"   ✅ Script: {script.get('title', 'Generated')}")
        print(f"   📊 Scenes: {len(script.get('scenes', []))}")
        
        # Test 3: Video creation
        print("\\n🎬 Test 3: Video Creation")
        result = engine.create_simple_video(script, "finance")
        
        if result:
            print(f"   ✅ Created: {os.path.basename(result)}")
        else:
            print("   ❌ Creation failed")
        
        print("\\n🎯 Testing complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure video_engine_core.py is in the current directory")
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_video_assistant():
    """Test interactive video assistant"""
    print("\\n🎬 Testing Video Assistant")
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
'''
    
    with open("test_video_creation.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Created: test_video_creation.py")

def update_requirements():
    """Update requirements.txt with video dependencies"""
    print("\n📋 Updating requirements.txt...")
    
    video_requirements = """
# Phase 4.2 Video Creation Dependencies
opencv-python>=4.8.0
Pillow>=10.0.0
matplotlib>=3.7.0
numpy>=1.24.0

# Optional video processing
moviepy>=1.0.3
imageio>=2.31.0
imageio-ffmpeg>=0.4.8

# Existing dependencies (keep these)
azure-identity>=1.15.0
azure-keyvault-secrets>=4.7.0
azure-cognitiveservices-speech>=1.34.0
azure-ai-translation-text>=1.0.0
openai>=1.6.1
fastapi>=0.104.1
requests>=2.31.0
"""
    
    # Read existing requirements if any
    existing_req = ""
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", 'r') as f:
            existing_content = f.read()
            # Keep non-video requirements
            lines = existing_content.split('\n')
            existing_req = '\n'.join([line for line in lines 
                                    if not any(pkg in line.lower() for pkg in 
                                              ['opencv', 'pillow', 'matplotlib', 'moviepy', 'imageio'])])
    
    # Combine requirements
    combined_requirements = existing_req + video_requirements
    
    with open("requirements.txt", 'w') as f:
        f.write(combined_requirements)
    
    print("✅ Updated requirements.txt with video dependencies")

def main():
    """Main setup function"""
    print("🎬 PHASE 4.2 VIDEO CREATION SETUP")
    print("=" * 45)
    print("Setting up AI-powered video creation environment...")
    
    try:
        # Step 1: Create directories
        create_directories()
        
        # Step 2: Install dependencies  
        install_video_dependencies()
        
        # Step 3: Create templates
        create_video_templates()
        
        # Step 4: Create assets
        create_sample_assets()
        
        # Step 5: Create test script
        create_test_script()
        
        # Step 6: Update requirements
        update_requirements()
        
        print("\n🎉 PHASE 4.2 VIDEO SETUP COMPLETE!")
        print("=" * 40)
        print("✅ Video processing environment ready")
        print("✅ Professional templates created")
        print("✅ Chennai business themes configured")
        print("✅ Test scripts generated")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Test video engine: python test_video_creation.py")
        print("2. Launch assistant: python rudh_video_assistant_v42.py")
        print("3. Create your first video!")
        
        print("\n💡 EXAMPLE COMMANDS:")
        print("   'Create a video about AI portfolio management'")
        print("   'Make a presentation on Chennai tech opportunities'")
        print("   'Generate tutorial for investment strategies'")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("💡 Try running individual setup steps manually")

if __name__ == "__main__":
    main()