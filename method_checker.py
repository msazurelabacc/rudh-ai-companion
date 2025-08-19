# method_checker.py - Check what methods are available in your services
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from azure_speech_service import AzureSpeechService
    from azure_openai_service import AzureOpenAIService
    
    print("🔍 CHECKING SERVICE METHODS...")
    
    # Check Speech Service methods
    print("\n🗣️ AZURE SPEECH SERVICE METHODS:")
    speech_service = AzureSpeechService()
    speech_methods = [m for m in dir(speech_service) if not m.startswith('_') and callable(getattr(speech_service, m))]
    for method in speech_methods:
        print(f"   ✅ {method}")
    
    # Check OpenAI Service methods  
    print("\n🤖 AZURE OPENAI SERVICE METHODS:")
    ai_service = AzureOpenAIService()
    ai_methods = [m for m in dir(ai_service) if not m.startswith('_') and callable(getattr(ai_service, m))]
    for method in ai_methods:
        print(f"   ✅ {method}")
        
    print(f"\n🎯 RECOMMENDED FIXES:")
    
    # Recommend speech method
    if 'synthesize_speech' in speech_methods:
        print("   🗣️ Use: speech_service.synthesize_speech(text)")
    elif 'speak' in speech_methods:
        print("   🗣️ Use: speech_service.speak(text)")
    elif 'text_to_speech' in speech_methods:
        print("   🗣️ Use: speech_service.text_to_speech(text)")
    else:
        print(f"   🗣️ Available: {speech_methods}")
    
    # Recommend AI method
    if 'get_response' in ai_methods:
        print("   🤖 Use: ai_service.get_response(prompt)")
    elif 'generate_response' in ai_methods:
        print("   🤖 Use: ai_service.generate_response(prompt)")
    elif 'get_completion' in ai_methods:
        print("   🤖 Use: ai_service.get_completion(prompt)")
    else:
        print(f"   🤖 Available: {ai_methods}")
        
except Exception as e:
    print(f"Error checking methods: {e}")
    print("Please ensure azure_speech_service.py and azure_openai_service.py exist in src/ directory")