# fix_moviepy_path.py
"""
Fix MoviePy Path Issues and Test Installation
Resolves import issues and verifies MoviePy functionality
"""

import sys
import os
import subprocess

def check_python_path():
    """Check Python path and MoviePy installation"""
    print("🔍 Checking Python Environment")
    print("=" * 35)
    
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path entries: {len(sys.path)}")
    
    # Check if MoviePy is in installed packages
    result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                          capture_output=True, text=True)
    
    if "moviepy" in result.stdout.lower():
        print("✅ MoviePy found in pip list")
        
        # Get MoviePy location
        result = subprocess.run([sys.executable, "-m", "pip", "show", "moviepy"], 
                              capture_output=True, text=True)
        print(f"📁 MoviePy info:")
        for line in result.stdout.split('\n'):
            if line.startswith('Location:') or line.startswith('Version:'):
                print(f"   {line}")
    else:
        print("❌ MoviePy not found in pip list")

def force_moviepy_import():
    """Force import MoviePy with path fixes"""
    print("\n🔧 Attempting MoviePy Import with Path Fixes")
    print("=" * 50)
    
    try:
        # Try direct import first
        import moviepy
        print("✅ MoviePy base import successful")
        print(f"📁 MoviePy location: {moviepy.__file__}")
        
        # Try editor import
        from moviepy.editor import VideoFileClip, ImageClip
        print("✅ MoviePy editor import successful")
        
        # Try effects import
        from moviepy.video.fx import fadein, fadeout
        print("✅ MoviePy effects import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ MoviePy import failed: {e}")
        
        # Try adding common MoviePy paths
        possible_paths = [
            r"C:\Python313\Lib\site-packages",
            r"C:\Python313\lib\site-packages", 
            r"C:\Users\{}\AppData\Local\Programs\Python\Python313\Lib\site-packages".format(os.getenv('USERNAME', '')),
            r"C:\Users\{}\AppData\Roaming\Python\Python313\site-packages".format(os.getenv('USERNAME', ''))
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
                print(f"📁 Added to path: {path}")
        
        # Try import again
        try:
            import moviepy
            from moviepy.editor import VideoFileClip, ImageClip
            from moviepy.video.fx import fadein, fadeout
            print("✅ MoviePy import successful after path fix")
            return True
        except ImportError as e:
            print(f"❌ MoviePy import still failed: {e}")
            return False

def reinstall_moviepy():
    """Reinstall MoviePy with verbose output"""
    print("\n🔄 Reinstalling MoviePy")
    print("=" * 25)
    
    try:
        # Uninstall first
        print("📤 Uninstalling MoviePy...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "moviepy", "-y"], 
                      check=True)
        
        # Reinstall with verbose output
        print("📥 Reinstalling MoviePy...")
        subprocess.run([sys.executable, "-m", "pip", "install", "moviepy", "--verbose"], 
                      check=True)
        
        print("✅ MoviePy reinstallation complete")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Reinstallation failed: {e}")
        return False

def create_simple_moviepy_test():
    """Create a simple test to verify MoviePy works"""
    print("\n🧪 Creating Simple MoviePy Test")
    print("=" * 35)
    
    test_code = '''
import sys
import os

try:
    from moviepy.editor import ImageClip, concatenate_videoclips
    from moviepy.video.fx import fadein, fadeout
    from PIL import Image
    
    print("✅ All imports successful")
    
    # Create simple test
    img = Image.new('RGB', (640, 480), color='red')
    img.save("test_slide.png")
    
    clip = ImageClip("test_slide.png", duration=2.0)
    clip = clip.set_fps(24)
    clip = fadein(clip, 0.5)
    
    print("✅ Basic MoviePy operations successful")
    
    # Clean up
    clip.close()
    if os.path.exists("test_slide.png"):
        os.remove("test_slide.png")
    
    print("✅ MoviePy test completed successfully")
    
except Exception as e:
    print(f"❌ MoviePy test failed: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Write test file
    with open("moviepy_simple_test.py", "w") as f:
        f.write(test_code)
    
    print("📝 Created moviepy_simple_test.py")
    
    # Run test
    try:
        result = subprocess.run([sys.executable, "moviepy_simple_test.py"], 
                              capture_output=True, text=True, timeout=30)
        
        print("📋 Test output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Test errors:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def main():
    """Main fix procedure"""
    print("🔧 MOVIEPY PATH FIX AND VERIFICATION")
    print("=" * 45)
    
    # Step 1: Check environment
    check_python_path()
    
    # Step 2: Try import with path fixes
    if force_moviepy_import():
        print("\n🎉 MoviePy is working!")
        
        # Create updated engine test
        print("\n🚀 Creating Updated Engine Test")
        updated_test = '''
# Quick test of fixed MoviePy integration
import sys
sys.path.insert(0, r"C:\\Python313\\Lib\\site-packages")

try:
    from moviepy.editor import ImageClip
    print("✅ MoviePy working in engine context")
    
    # Test basic functionality
    from PIL import Image
    img = Image.new('RGB', (100, 100), 'blue')
    img.save("quick_test.png")
    
    clip = ImageClip("quick_test.png", duration=1.0)
    print(f"✅ Created clip: {clip.duration}s")
    
    clip.close()
    import os
    if os.path.exists("quick_test.png"):
        os.remove("quick_test.png")
    
    print("✅ MoviePy fully operational!")
    
except Exception as e:
    print(f"❌ Engine test failed: {e}")
'''
        
        with open("test_engine_moviepy.py", "w") as f:
            f.write(updated_test)
        
        print("📝 Created test_engine_moviepy.py")
        print("\n💡 Run this to verify: python test_engine_moviepy.py")
        
    else:
        print("\n🔄 Attempting reinstallation...")
        if reinstall_moviepy():
            print("✅ Reinstallation successful, testing...")
            create_simple_moviepy_test()
        else:
            print("❌ Reinstallation failed")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Run: python test_engine_moviepy.py")
    print("2. If successful, run: python advanced_video_engine_v43_fixed.py")
    print("3. Then try: python rudh_enhanced_video_assistant_v43_fixed.py")

if __name__ == "__main__":
    main()