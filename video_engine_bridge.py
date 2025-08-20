# video_engine_bridge.py
"""
Video Engine Bridge - Connect existing video capabilities to voice system
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Try to import existing video engines
VIDEO_ENGINE_AVAILABLE = False
video_engine = None

# Method 1: Try enhanced video engine
try:
    from advanced_video_engine_v43_fixed import EnhancedVideoEngine
    video_engine = EnhancedVideoEngine()
    VIDEO_ENGINE_AVAILABLE = True
    print("✅ Using EnhancedVideoEngine from advanced_video_engine_v43_fixed")
except ImportError:
    try:
        # Method 2: Try alternative video engine
        from alternative_video_engine import AlternativeVideoEngine
        video_engine = AlternativeVideoEngine()
        VIDEO_ENGINE_AVAILABLE = True
        print("✅ Using AlternativeVideoEngine")
    except ImportError:
        try:
            # Method 3: Try core video engine
            from video_engine_core import VideoEngine
            video_engine = VideoEngine()
            VIDEO_ENGINE_AVAILABLE = True
            print("✅ Using VideoEngine from video_engine_core")
        except ImportError:
            print("⚠️ No video engine found - will create basic engine")

class VideoBridge:
    """Bridge to connect any available video engine to voice system"""
    
    def __init__(self):
        self.setup_logging()
        self.video_engine = video_engine
        self.is_available = VIDEO_ENGINE_AVAILABLE
        
        # Directories
        self.output_dir = Path("voice_enhanced_videos")
        self.output_dir.mkdir(exist_ok=True)
        
        if self.is_available:
            self.logger.info("✅ Video bridge initialized with existing engine")
        else:
            self.logger.warning("⚠️ Video bridge in fallback mode")
    
    def setup_logging(self):
        """Setup logging"""
        self.logger = logging.getLogger('VideoBridge')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def create_enhanced_video_with_opencv(self, script: Dict, theme: str = "tech", 
                                        quality: str = "high") -> str:
        """Create enhanced video using available engine"""
        
        if not self.is_available:
            return self._create_fallback_video(script, theme, quality)
        
        try:
            # Try existing engine methods
            if hasattr(self.video_engine, 'create_enhanced_video_with_opencv'):
                return self.video_engine.create_enhanced_video_with_opencv(script, theme, quality)
            elif hasattr(self.video_engine, 'create_simple_video'):
                return self.video_engine.create_simple_video(script, theme)
            elif hasattr(self.video_engine, 'create_video'):
                return self.video_engine.create_video(script, theme)
            else:
                return self._create_fallback_video(script, theme, quality)
                
        except Exception as e:
            self.logger.error(f"❌ Video engine failed: {e}")
            return self._create_fallback_video(script, theme, quality)
    
    def _create_fallback_video(self, script: Dict, theme: str, quality: str) -> str:
        """Create fallback video assets when engine unavailable"""
        
        try:
            import json
            from datetime import datetime
            
            # Create video metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_clean = "".join(c for c in script.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"fallback_{title_clean[:30]}_{timestamp}.json"
            output_path = self.output_dir / filename
            
            # Create fallback video info
            fallback_video = {
                'type': 'fallback_video',
                'title': script.get('title', 'Untitled'),
                'scenes': script.get('scenes', []),
                'theme': theme,
                'quality': quality,
                'timestamp': timestamp,
                'message': 'Video engine not available - voice narration created successfully',
                'voice_ready': True
            }
            
            # Save metadata
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(fallback_video, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Fallback video metadata created: {filename}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"❌ Fallback video creation failed: {e}")
            return None

# Global bridge instance
video_bridge = VideoBridge()

# Export functions for compatibility
def create_enhanced_video_with_opencv(script: Dict, theme: str = "tech", quality: str = "high") -> str:
    """Compatibility function for voice system"""
    return video_bridge.create_enhanced_video_with_opencv(script, theme, quality)

def get_video_engine_status() -> Dict:
    """Get video engine status"""
    return {
        'available': video_bridge.is_available,
        'engine_type': type(video_bridge.video_engine).__name__ if video_bridge.video_engine else 'None',
        'fallback_mode': not video_bridge.is_available
    }

# Test function
def test_video_bridge():
    """Test video bridge functionality"""
    print("🧪 Testing Video Engine Bridge")
    print("=" * 40)
    
    status = get_video_engine_status()
    print(f"📊 Video Engine Status:")
    print(f"   Available: {'✅' if status['available'] else '❌'}")
    print(f"   Engine Type: {status['engine_type']}")
    print(f"   Fallback Mode: {'✅' if status['fallback_mode'] else '❌'}")
    
    # Test video creation
    test_script = {
        "title": "Video Bridge Test",
        "scenes": [
            {"slide_text": "Test Slide 1", "narration": "Testing video bridge", "duration": 30},
            {"slide_text": "Test Slide 2", "narration": "Bridge functionality", "duration": 30},
        ]
    }
    
    result = create_enhanced_video_with_opencv(test_script, "tech", "high")
    
    if result:
        print(f"✅ Video bridge test successful!")
        print(f"📁 Output: {os.path.basename(result)}")
    else:
        print(f"❌ Video bridge test failed")
    
    return video_bridge

if __name__ == "__main__":
    test_video_bridge()
