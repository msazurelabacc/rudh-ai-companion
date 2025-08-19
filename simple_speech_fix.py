# simple_speech_fix.py
"""
Quick fix for Azure Speech Service - Use simple text instead of complex SSML
"""

import asyncio
import os
import sys
sys.path.append('src')

from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

async def test_simple_speech():
    """Test with simple text synthesis (no SSML)"""
    print("🔧 TESTING SIMPLE SPEECH SYNTHESIS")
    print("=" * 50)
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'southeastasia')
    speech_voice = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
    
    print(f"📋 Configuration:")
    print(f"   Region: {speech_region}")
    print(f"   Voice: {speech_voice}")
    
    if not speech_key:
        print("❌ Missing speech key")
        return
    
    try:
        # Create speech config
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        speech_config.speech_synthesis_voice_name = speech_voice
        
        # SIMPLE APPROACH: Use default audio output
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None  # Let Azure SDK handle audio output automatically
        )
        
        print(f"\n🎵 Testing simple text synthesis...")
        
        # Test simple text (NO SSML)
        test_text = "Hello! I'm Rudh, your AI companion. How are you feeling today?"
        
        result = synthesizer.speak_text_async(test_text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✅ SUCCESS! Simple text synthesis working!")
            print(f"   Audio size: {len(result.audio_data)} bytes")
            print(f"   Voice: {speech_voice}")
            return True
        else:
            print(f"❌ FAILED: {result.reason}")
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speechsdk.CancellationDetails(result)
                print(f"   Error: {cancellation_details.error_details}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def test_basic_ssml():
    """Test with very basic SSML"""
    print(f"\n🧪 TESTING BASIC SSML")
    print("=" * 30)
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'southeastasia')
    speech_voice = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
    
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_voice_name = speech_voice
        
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        # Very basic SSML - just voice selection
        basic_ssml = f'''
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-IN">
            <voice name="{speech_voice}">
                Hello! This is a basic SSML test.
            </voice>
        </speak>
        '''
        
        result = synthesizer.speak_ssml_async(basic_ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✅ Basic SSML works!")
            return True
        else:
            print(f"❌ Basic SSML failed: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ Basic SSML exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing different speech synthesis approaches...")
    
    # Test 1: Simple text
    success1 = asyncio.run(test_simple_speech())
    
    # Test 2: Basic SSML if simple works
    if success1:
        success2 = asyncio.run(test_basic_ssml())
    
    print(f"\n🎯 RESULTS:")
    print(f"   Simple Text: {'✅' if success1 else '❌'}")
    if success1:
        print(f"   Basic SSML: {'✅' if 'success2' in locals() and success2 else '❌'}")
    
    print(f"\n💡 RECOMMENDATION:")
    if success1:
        print("✅ Use simple text synthesis - skip complex SSML for now")
        print("🔧 Update your main app to use speak_text_async() instead of speak_ssml_async()")
    else:
        print("❌ Check Azure Speech Service configuration in portal")