# simple_speech_test.py
"""
Simple test for Azure Speech Service to identify the exact issue
"""

import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

def test_speech_service():
    """Test speech service with detailed error reporting"""
    print("🧪 TESTING AZURE SPEECH SERVICE")
    print("=" * 50)
    
    # Get credentials
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'southeastasia')
    speech_voice = os.getenv('AZURE_SPEECH_VOICE', 'en-IN-NeerjaNeural')
    
    print(f"📋 Configuration:")
    print(f"   Region: {speech_region}")
    print(f"   Voice: {speech_voice}")
    print(f"   Key Present: {'✅' if speech_key else '❌'}")
    
    if not speech_key:
        print("❌ AZURE_SPEECH_KEY not found in .env file")
        return False
    
    try:
        # Create speech config
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        
        # Set voice
        speech_config.speech_synthesis_voice_name = speech_voice
        
        print(f"\n🔧 Creating synthesizer...")
        
        # Create synthesizer with null audio config (don't play, just generate)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        print(f"✅ Synthesizer created successfully")
        
        # Test simple synthesis
        test_text = "Hello from Rudh. This is a speech test."
        print(f"\n🎵 Testing synthesis: '{test_text}'")
        
        result = synthesizer.speak_text_async(test_text).get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✅ SUCCESS! Speech synthesis working!")
            print(f"   Audio generated: {len(result.audio_data)} bytes")
            print(f"   Voice used: {speech_voice}")
            print(f"   Region used: {speech_region}")
            return True
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            print(f"❌ SYNTHESIS CANCELED")
            cancellation_details = speechsdk.CancellationDetails(result)
            print(f"   Reason: {cancellation_details.reason}")
            print(f"   Error Code: {cancellation_details.error_code}")
            if cancellation_details.error_details:
                print(f"   Error Details: {cancellation_details.error_details}")
            
            # Common error solutions
            print(f"\n💡 POTENTIAL SOLUTIONS:")
            if "authentication" in str(cancellation_details.error_details).lower():
                print("   🔑 Check your speech service key in Azure Portal")
                print("   🔄 Regenerate the key if needed")
            elif "region" in str(cancellation_details.error_details).lower():
                print("   🌏 Verify speech service region in Azure Portal")
                print("   📍 Current region setting: southeastasia")
            elif "voice" in str(cancellation_details.error_details).lower():
                print("   🗣️ Try a different voice: en-US-AriaNeural")
            
            return False
        else:
            print(f"❌ UNEXPECTED RESULT: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def test_alternative_voices():
    """Test with alternative voices if main one fails"""
    print(f"\n🧪 TESTING ALTERNATIVE VOICES")
    print("=" * 30)
    
    alternative_voices = [
        "en-US-AriaNeural",
        "en-US-JennyNeural", 
        "en-AU-NatashaNeural",
        "en-IN-PrabhatNeural"  # Male Indian voice
    ]
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION', 'southeastasia')
    
    if not speech_key:
        return
    
    for voice in alternative_voices:
        print(f"\n🎵 Testing voice: {voice}")
        
        try:
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            speech_config.speech_synthesis_voice_name = voice
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            )
            
            result = synthesizer.speak_text_async("Test voice").get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"✅ {voice} works! ({len(result.audio_data)} bytes)")
            else:
                print(f"❌ {voice} failed")
                
        except Exception as e:
            print(f"❌ {voice} error: {e}")

if __name__ == "__main__":
    success = test_speech_service()
    
    if not success:
        test_alternative_voices()
        
    print(f"\n🎯 SUMMARY:")
    if success:
        print("✅ Speech service working - check your main app configuration")
    else:
        print("❌ Speech service needs attention - check key and region")
        print("💡 Verify in Azure Portal: speech-rudh-core-dev-sea service")