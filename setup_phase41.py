# setup_phase41.py
"""
Phase 4.1 Setup Script - Creative Capabilities
Install dependencies and setup environment for Rudh Creative Assistant
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed: {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package}")
        return False

def setup_creative_environment():
    """Setup the creative content environment"""
    print("🎨 RUDH CREATIVE ASSISTANT V4.1 SETUP")
    print("=" * 60)
    print("Setting up creative content generation environment...")
    print("This will install dependencies for diagram generation and content creation.\n")
    
    # Required packages for creative capabilities
    packages = [
        # Core graphics and diagram generation
        "graphviz",
        "matplotlib",
        "pillow",
        "drawsvg",
        
        # Document and content generation
        "python-pptx",
        "reportlab",
        "jinja2",
        "markdown",
        
        # Additional utilities
        "pathlib",
        "python-dotenv",
        
        # Optional but recommended
        "cairosvg",  # For SVG to PNG conversion
        "selenium",  # For web-based content generation
    ]
    
    print("📦 Installing creative content packages...")
    success_count = 0
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"✅ Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count < len(packages):
        print("⚠️ Some packages failed to install. Creative features may be limited.")
        print("💡 Try installing manually: pip install <package_name>")
    
    # Setup directories
    print("\n📁 Creating creative directories...")
    directories = [
        "templates",
        "creative_output", 
        "assets",
        "templates/diagrams",
        "templates/content",
        "assets/fonts",
        "assets/images"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    # Check system dependencies
    print("\n🔧 Checking system dependencies...")
    
    # Check if Graphviz is installed system-wide
    try:
        subprocess.run(["dot", "-V"], capture_output=True, check=True)
        print("✅ Graphviz system installation found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Graphviz not found in system PATH")
        print("💡 Install Graphviz from: https://graphviz.org/download/")
        print("   Windows: Download and install from website")
        print("   macOS: brew install graphviz")
        print("   Linux: sudo apt-get install graphviz")
    
    # Create sample templates
    print("\n📝 Creating sample templates...")
    create_sample_templates()
    
    print("\n🎉 Setup complete!")
    print("\n🚀 Next steps:")
    print("1. Run: python creative_engine_core.py (test core engine)")
    print("2. Run: python rudh_creative_assistant_v41.py (start creative assistant)")
    print("3. Try commands like: 'create diagram architecture' or 'templates'")

def create_sample_templates():
    """Create sample templates for users to start with"""
    
    # Sample architecture diagram template
    arch_template = """# Architecture Diagram Template

## Components:
- Frontend: User Interface Layer
- API Gateway: Request Routing and Authentication  
- Business Logic: Core Application Logic
- Database: Data Persistence Layer
- Cache: Performance Optimization

## Connections:
- User → Frontend → API Gateway → Business Logic → Database
- Business Logic ↔ Cache (bidirectional)

## Notes:
- Use this template as a starting point for system architecture diagrams
- Customize components and connections for your specific system
"""
    
    with open("templates/architecture_template.md", "w") as f:
        f.write(arch_template)
    
    # Sample presentation template
    pres_template = """# Business Presentation Template

## Title Slide
- Presentation Title
- Presenter Name
- Company/Organization
- Date

## Agenda
1. Problem Statement
2. Solution Overview
3. Benefits and Value
4. Implementation Plan
5. Next Steps

## Problem Statement
- Current challenges
- Impact and pain points
- Market opportunity

## Solution Overview
- Proposed solution
- Key features
- Technical approach

## Benefits and Value
- Business benefits
- Cost savings
- Competitive advantages

## Implementation Plan
- Timeline and milestones
- Resource requirements
- Risk mitigation

## Next Steps
- Immediate actions
- Decision points
- Contact information
"""
    
    with open("templates/presentation_template.md", "w") as f:
        f.write(pres_template)
    
    print("✅ Created sample templates")

if __name__ == "__main__":
    setup_creative_environment()