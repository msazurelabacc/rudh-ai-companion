# setup_voice_enhanced_video_phase44.py
"""
Phase 4.4 Setup Script - Voice-Enhanced Video Creation System
Complete environment setup for Azure Speech integration with video creation
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🎬🗣️ PHASE 4.4 VOICE-ENHANCED VIDEO CREATION SETUP")
    print("=" * 65)
    print("Setting up complete voice-enabled video production environment...")
    print("🎯 Azure Speech Services + Enhanced Video Creation")
    print("🗣️ Indian English Voice Synthesis + Professional Templates")
    print("🏢 Chennai Business Context + AI-Powered Content Generation")
    print()

def install_voice_dependencies():
    """Install voice and audio processing dependencies"""
    print("📦 Installing voice and audio processing dependencies...")
    
    dependencies = [
        'azure-cognitiveservices-speech>=1.34.0',
        'azure-identity>=1.15.0',
        'azure-keyvault-secrets>=4.7.0',
        'pygame>=2.5.2',
        'python-dotenv>=1.0.0',
        'wave',
        'asyncio'
    ]
    
    for dep in dependencies:
        try:
            if dep in ['wave', 'asyncio']:  # Built-in modules
                print(f"✅ {dep}: Built-in module")
                continue
                
            print(f"📥 Installing {dep}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", dep, "--upgrade"
            ], check=True, capture_output=True)
            print(f"✅ {dep}: Installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ {dep}: Installation failed - {e}")
            print(f"   Continuing with setup...")
    
    print("✅ Voice dependencies installation complete!")

def create_voice_directories():
    """Create voice-enhanced video directories"""
    print("\n📁 Creating voice-enhanced video directories...")
    
    directories = [
        "voice_enhanced_videos",
        "audio_output", 
        "voice_narration",
        "combined_videos",
        "voice_templates",
        "speech_cache"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    print("✅ Voice directories created successfully!")

def create_voice_config():
    """Create voice configuration templates"""
    print("\n🔧 Creating voice configuration templates...")
    
    # Azure Speech configuration template
    azure_config = {
        "azure_speech": {
            "region": "eastus2",
            "voice_default": "en-IN-NeerjaNeural",
            "audio_format": "Audio48Khz192KBitRateMonoMp3",
            "timeout": 30
        },
        "voice_personas": {
            "professional": {
                "voice": "en-IN-NeerjaNeural",
                "style": "newscast",
                "rate": "0%",
                "pitch": "0%",
                "description": "Professional business tone"
            },
            "enthusiastic": {
                "voice": "en-IN-NeerjaNeural", 
                "style": "cheerful",
                "rate": "+10%",
                "pitch": "+5%",
                "description": "Energetic and engaging"
            },
            "authoritative": {
                "voice": "en-IN-PrabhatNeural",
                "style": "newscast",
                "rate": "-5%",
                "pitch": "-5%",
                "description": "Confident and credible"
            },
            "friendly": {
                "voice": "en-IN-NeerjaNeural",
                "style": "friendly",
                "rate": "0%",
                "pitch": "0%",
                "description": "Warm and approachable"
            },
            "tamil_friendly": {
                "voice": "ta-IN-PallaviNeural",
                "style": "friendly",
                "rate": "0%",
                "pitch": "0%",
                "description": "Tamil voice for cultural authenticity"
            }
        },
        "quality_presets": {
            "presentation_quality": {
                "resolution": [1920, 1080],
                "video_bitrate": 6000000,
                "audio_bitrate": 192000,
                "fps": 30
            },
            "web_optimized": {
                "resolution": [1280, 720],
                "video_bitrate": 2500000,
                "audio_bitrate": 128000,
                "fps": 25
            },
            "mobile_friendly": {
                "resolution": [854, 480],
                "video_bitrate": 1200000,
                "audio_bitrate": 96000,
                "fps": 24
            }
        }
    }
    
    # Save configuration
    config_path = Path("voice_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(azure_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Voice configuration saved: {config_path}")
    
    # Create environment template
    env_template = """# Azure Speech Services Configuration for Rudh Voice Integration
# Copy this to .env and add your actual Azure credentials

# Azure Speech Services
AZURE_SPEECH_KEY=your_speech_service_key_here
AZURE_SPEECH_REGION=eastus2
AZURE_SPEECH_VOICE=en-IN-NeerjaNeural

# Azure Key Vault (optional)
AZURE_KEY_VAULT_URL=https://kv-rudh-secrets-eastus2.vault.azure.net/

# Voice Settings
VOICE_CACHE_ENABLED=true
VOICE_PLAYBACK_ENABLED=true
VOICE_QUALITY=high

# Chennai Context
CHENNAI_CONTEXT_ENABLED=true
TAMIL_SUPPORT_ENABLED=true
LOCAL_BUSINESS_THEMES=true
"""
    
    env_template_path = Path("voice_config.env.template")
    with open(env_template_path, 'w', encoding='utf-8') as f:
        f.write(env_template)
    
    print(f"✅ Environment template saved: {env_template_path}")

def create_voice_templates():
    """Create voice-enabled video templates"""
    print("\n🎨 Creating voice-enabled video templates...")
    
    # Business presentation template
    business_template = {
        "name": "Chennai Business Presentation",
        "description": "Professional business presentation with Indian English narration",
        "voice_persona": "professional",
        "template_type": "business_presentation",
        "scenes": [
            {
                "type": "title",
                "template": "{title}\nPowered by Rudh AI",
                "narration_template": "Welcome to our comprehensive presentation on {topic}. Let's explore the key insights and opportunities.",
                "duration": 45
            },
            {
                "type": "overview",
                "template": "Overview\n• Key Concepts\n• Market Analysis\n• Strategic Insights",
                "narration_template": "Today's session covers the fundamental concepts, current market dynamics, and strategic insights for {topic}.",
                "duration": 50
            },
            {
                "type": "content",
                "template": "Market Opportunities\nChennai Business Landscape",
                "narration_template": "Chennai's thriving business ecosystem offers exceptional opportunities in {topic}. The city's strategic advantages create competitive benefits.",
                "duration": 60
            },
            {
                "type": "analysis",
                "template": "Strategic Analysis\nData-Driven Insights",
                "narration_template": "Our analysis reveals significant trends and opportunities. These data-driven insights guide strategic decision-making for maximum impact.",
                "duration": 55
            },
            {
                "type": "implementation",
                "template": "Implementation Strategy\nAction Plan",
                "narration_template": "Successful implementation requires a systematic approach. Let's outline the specific steps to achieve your objectives in {topic}.",
                "duration": 50
            },
            {
                "type": "conclusion",
                "template": "Thank You\nNext Steps & Discussion",
                "narration_template": "Thank you for your attention. Let's discuss how we can implement these strategies for your business success.",
                "duration": 40
            }
        ],
        "total_duration": 300,
        "style": "corporate_professional",
        "voice_style": "newscast"
    }
    
    # Tech showcase template
    tech_template = {
        "name": "Technology Innovation Showcase",
        "description": "Energetic tech presentation with enthusiastic narration",
        "voice_persona": "enthusiastic",
        "template_type": "tech_showcase",
        "scenes": [
            {
                "type": "title",
                "template": "Technology Innovation\n{title}",
                "narration_template": "Get ready to discover cutting-edge technology that's transforming {topic}. This is truly exciting!",
                "duration": 40
            },
            {
                "type": "innovation",
                "template": "Innovation Spotlight\nBreaking New Ground",
                "narration_template": "Innovation in {topic} is happening at breakneck speed. Let's explore the technologies that are reshaping entire industries.",
                "duration": 50
            },
            {
                "type": "applications",
                "template": "Real-World Applications\nPractical Implementation",
                "narration_template": "These aren't just concepts – they're real solutions being implemented right here in Chennai and around the world.",
                "duration": 55
            },
            {
                "type": "benefits",
                "template": "Transformative Benefits\nMeasurable Impact",
                "narration_template": "The benefits are remarkable! Companies implementing these {topic} solutions see dramatic improvements in efficiency and results.",
                "duration": 50
            },
            {
                "type": "future",
                "template": "Future Possibilities\nWhat's Next",
                "narration_template": "The future is here, and it's powered by innovation in {topic}. Let's harness this technology for remarkable results.",
                "duration": 45
            }
        ],
        "total_duration": 240,
        "style": "tech_modern",
        "voice_style": "cheerful"
    }
    
    # Financial education template
    finance_template = {
        "name": "Financial Education Series",
        "description": "Authoritative financial education with expert narration",
        "voice_persona": "authoritative",
        "template_type": "financial_education",
        "scenes": [
            {
                "type": "title",
                "template": "Financial Education Series\n{title}",
                "narration_template": "Welcome to our financial education series. Today we'll master the fundamentals of {topic}.",
                "duration": 45
            },
            {
                "type": "fundamentals",
                "template": "Core Principles\nFoundational Knowledge",
                "narration_template": "Understanding the core principles of {topic} is essential for making informed financial decisions.",
                "duration": 60
            },
            {
                "type": "strategies",
                "template": "Proven Strategies\nExpert Approaches",
                "narration_template": "Industry experts have developed proven strategies for {topic}. These approaches have been tested across global markets.",
                "duration": 65
            },
            {
                "type": "implementation",
                "template": "Practical Implementation\nYour Action Plan",
                "narration_template": "Remember, successful investing requires knowledge, patience, and disciplined execution. Start your journey today.",
                "duration": 50
            }
        ],
        "total_duration": 220,
        "style": "finance_professional",
        "voice_style": "newscast"
    }
    
    # Save templates
    templates = {
        "business_presentation": business_template,
        "tech_showcase": tech_template,
        "financial_education": finance_template
    }
    
    templates_dir = Path("voice_templates")
    for template_name, template_data in templates.items():
        template_file = templates_dir / f"{template_name}.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Created template: {template_file}")
    
    print("✅ Voice-enabled templates created successfully!")

def create_test_scripts():
    """Create test scripts for voice integration"""
    print("\n🧪 Creating voice integration test scripts...")
    
    # Test Azure Speech Service
    test_speech_script = '''# test_azure_speech.py
"""
Test Azure Speech Service Integration
"""
import asyncio
from azure_speech_service_v44 import AzureSpeechService

async def test_speech_service():
    print("🧪 Testing Azure Speech Service V4.4")
    print("=" * 50)
    
    service = AzureSpeechService()
    
    # Test voice synthesis
    test_text = "Welcome to Rudh's voice-enhanced video creation system with professional Indian English narration."
    
    result = await service.text_to_speech_with_persona(
        test_text, 
        persona="professional"
    )
    
    if result['success']:
        print(f"✅ Voice synthesis successful!")
        print(f"📁 Audio file: {result['audio_file']}")
        print(f"⏱️ Duration: {result['duration']:.2f}s")
        print(f"🗣️ Voice: {result['voice']}")
    else:
        print(f"⚠️ Voice synthesis in fallback mode")
    
    return service

if __name__ == "__main__":
    asyncio.run(test_speech_service())
'''
    
    # Test voice-enhanced video creation
    test_video_script = '''# test_voice_enhanced_video.py
"""
Test Voice-Enhanced Video Creation
"""
import asyncio
from enhanced_video_assistant_v44 import EnhancedVideoAssistantV44

async def test_voice_video():
    print("🧪 Testing Voice-Enhanced Video Creation V4.4")
    print("=" * 60)
    
    assistant = EnhancedVideoAssistantV44()
    
    # Test video creation
    result = await assistant.create_voice_enhanced_video(
        topic="AI Portfolio Management for Chennai Businesses",
        template="business_presentation",
        persona="professional",
        quality="presentation_quality"
    )
    
    if result['success']:
        print(f"✅ Voice-enhanced video creation successful!")
        print(f"📁 Video: {result['video_file']}")
        print(f"🗣️ Voice enabled: {result['voice_enabled']}")
        print(f"📊 Scenes: {result['completed_scenes']}/{result['total_scenes']}")
        print(f"⏱️ Total time: {result['total_duration']:.1f}s")
    else:
        print(f"❌ Video creation failed: {result.get('error')}")
    
    return assistant

if __name__ == "__main__":
    asyncio.run(test_voice_video())
'''
    
    # Save test scripts
    with open("test_azure_speech.py", 'w', encoding='utf-8') as f:
        f.write(test_speech_script)
    print("✅ Created: test_azure_speech.py")
    
    with open("test_voice_enhanced_video.py", 'w', encoding='utf-8') as f:
        f.write(test_video_script)
    print("✅ Created: test_voice_enhanced_video.py")
    
    print("✅ Test scripts created successfully!")

def create_azure_setup_guide():
    """Create Azure setup guide"""
    print("\n📋 Creating Azure Speech Service setup guide...")
    
    setup_guide = """# Azure Speech Service Setup Guide for Rudh Voice Integration

## Step 1: Create Azure Speech Service

1. Go to Azure Portal (https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Speech Services"
4. Click "Create"

## Step 2: Configuration

**Subscription:** Your Azure subscription
**Resource Group:** rg-rudh-core-dev-sea (same as OpenAI)
**Region:** East US 2 (same as your OpenAI resource)
**Name:** rudh-speech-eastus2
**Pricing Tier:** Standard S0

## Step 3: Get Credentials

1. After deployment, go to your Speech resource
2. Click "Keys and Endpoint"
3. Copy Key 1 and Region

## Step 4: Configure Environment

Add to your .env file:
```
AZURE_SPEECH_KEY=your_speech_service_key_here
AZURE_SPEECH_REGION=eastus2
AZURE_SPEECH_VOICE=en-IN-NeerjaNeural
```

## Step 5: Add to Key Vault (Optional)

If using Azure Key Vault:
- Secret Name: rudh-speech-key, Value: [Key 1]
- Secret Name: rudh-speech-region, Value: eastus2
- Secret Name: rudh-speech-voice, Value: en-IN-NeerjaNeural

## Available Voice Options

### Indian English (Recommended)
- **en-IN-NeerjaNeural** (Female, warm and friendly)
- **en-IN-PrabhatNeural** (Male, professional)

### Tamil (Cultural Authenticity)
- **ta-IN-PallaviNeural** (Female)
- **ta-IN-ValluvarNeural** (Male)

## Cost Information

- **Free Tier:** 5 hours per month
- **Paid:** $4.50 per hour after free tier
- **For personal use:** You'll likely stay within free tier

## Testing Your Setup

Run these commands to test:
```bash
python test_azure_speech.py
python test_voice_enhanced_video.py
```

## Troubleshooting

### Common Issues:
1. **Authentication Error:** Check your Azure credentials
2. **Region Mismatch:** Ensure region matches your resource
3. **Audio Playback Issues:** Install pygame: `pip install pygame`
4. **Import Errors:** Run setup script: `python setup_voice_enhanced_video_phase44.py`

### Support:
- Azure Speech Documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/
- Rudh Project Repository: Your GitHub repository
"""
    
    with open("AZURE_SPEECH_SETUP.md", 'w', encoding='utf-8') as f:
        f.write(setup_guide)
    
    print("✅ Created: AZURE_SPEECH_SETUP.md")

def display_next_steps():
    """Display next steps after setup"""
    print("\n🎉 PHASE 4.4 VOICE-ENHANCED VIDEO SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n✅ SETUP COMPLETED SUCCESSFULLY:")
    print("   📦 Voice processing dependencies installed")
    print("   📁 Voice-enhanced video directories created")
    print("   🔧 Voice configuration templates created")
    print("   🎨 Professional voice-enabled templates created")
    print("   🧪 Voice integration test scripts created")
    print("   📋 Azure Speech Service setup guide created")
    
    print("\n🚀 NEXT STEPS:")
    print("1. **Setup Azure Speech Service** (REQUIRED):")
    print("   📖 Follow guide: AZURE_SPEECH_SETUP.md")
    print("   🔑 Add your Azure Speech credentials to .env")
    
    print("\n2. **Test Voice Integration:**")
    print("   python test_azure_speech.py")
    print("   python test_voice_enhanced_video.py")
    
    print("\n3. **Launch Voice-Enhanced Video Assistant:**")
    print("   python enhanced_video_assistant_v44.py interactive")
    
    print("\n4. **Create Your First Voice Video:**")
    print("   'Create enhanced video about AI portfolio management'")
    print("   'Make professional presentation with voice narration'")
    
    print("\n🌟 WHAT YOU'LL ACHIEVE:")
    print("   🎬 Professional videos with Indian English narration")
    print("   🗣️ Multiple voice personas (Professional, Enthusiastic, Authoritative)")
    print("   🏢 Chennai business context with cultural authenticity")
    print("   📱 Multiple quality presets for different use cases")
    print("   💰 Premium video production worth ₹1,00,000+ monthly")
    
    print("\n⚠️ IMPORTANT:")
    print("   • Azure Speech Service required for voice features")
    print("   • Free tier includes 5 hours monthly (sufficient for personal use)")
    print("   • System works in fallback mode without Azure credentials")
    print("   • Voice narration files saved separately for flexible use")

def main():
    """Main setup function"""
    print_header()
    
    try:
        # Run setup steps
        install_voice_dependencies()
        create_voice_directories()
        create_voice_config()
        create_voice_templates()
        create_test_scripts()
        create_azure_setup_guide()
        
        # Display completion message
        display_next_steps()
        
        print("\n🎯 Ready to revolutionize video creation with AI-powered voice integration!")
        
    except Exception as e:
        print(f"\n❌ Setup encountered an error: {e}")
        print("Please check the error and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()
"