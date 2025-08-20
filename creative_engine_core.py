# creative_engine_core.py - FIXED VERSION
"""
Rudh Creative Engine Core - Phase 4.1 FIXED
Advanced Content Creation with Fallback Support
"""

import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

# Try graphics libraries with fallbacks
GRAPHICS_AVAILABLE = False
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
    print("✅ Matplotlib available")
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib not available")

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
    print("✅ PIL available")
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL not available")

# Set graphics status
GRAPHICS_AVAILABLE = MATPLOTLIB_AVAILABLE or PIL_AVAILABLE

# Import existing Rudh components with fallbacks
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from azure_openai_service import AzureOpenAIService
    from azure_speech_service import AzureSpeechService
    print("✅ Azure services imported")
except ImportError as e:
    print(f"⚠️ Azure services import failed: {e}")
    # Fallback classes
    class AzureOpenAIService:
        def __init__(self):
            self.logger = logging.getLogger("AzureOpenAI")
            self.logger.warning("⚠️ Azure OpenAI service not available")
        
        async def get_response(self, prompt):
            return "AI service not available for creative analysis."
    
    class AzureSpeechService:
        def __init__(self):
            self.logger = logging.getLogger("AzureSpeech")
            self.logger.warning("⚠️ Azure Speech service not available")
        
        async def speak_text(self, text):
            print(f"🔊 Voice: {text}")


class CreativeEngine:
    """Core Creative Content Generation Engine - Fixed Version"""
    
    def __init__(self):
        self.logger = logging.getLogger("CreativeEngine")
        
        # Initialize AI services
        self.ai_service = AzureOpenAIService()
        self.speech_service = AzureSpeechService()
        
        # Creative capabilities
        self.templates_dir = Path("templates")
        self.output_dir = Path("creative_output")
        self.assets_dir = Path("assets")
        
        # Create directories
        self._setup_directories()
        
        # Graphics status
        self.graphics_enabled = GRAPHICS_AVAILABLE
        
        self.logger.info(f"✅ Creative Engine initialized (Graphics: {'✅' if self.graphics_enabled else '❌ Text Mode'})")
    
    def _setup_directories(self):
        """Setup creative content directories"""
        for directory in [self.templates_dir, self.output_dir, self.assets_dir]:
            directory.mkdir(exist_ok=True)
            self.logger.info(f"📁 Directory ready: {directory}")
    
    async def generate_technical_diagram(self, diagram_type: str, specification: str) -> Dict[str, Any]:
        """Generate technical diagrams based on AI analysis"""
        try:
            start_time = time.time()
            
            self.logger.info(f"🎨 Generating {diagram_type} diagram...")
            
            # AI-powered diagram analysis
            ai_prompt = f"""
            You are a technical diagram expert. Analyze this specification and create a structured diagram plan:
            
            Diagram Type: {diagram_type}
            Specification: {specification}
            
            Provide a JSON response with:
            - components: List of main components/nodes
            - connections: List of relationships between components
            - layout: Suggested layout (hierarchical, network, flow)
            - styling: Color scheme and visual suggestions
            - title: Descriptive title for the diagram
            """
            
            ai_response = await self.ai_service.get_response(ai_prompt)
            
            # Parse AI response (fallback to structured format if AI not available)
            if "AI service not available" in ai_response:
                diagram_plan = self._create_fallback_diagram_plan(diagram_type, specification)
            else:
                try:
                    # Try to extract JSON from AI response
                    import re
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        diagram_plan = json.loads(json_match.group())
                    else:
                        diagram_plan = self._create_fallback_diagram_plan(diagram_type, specification)
                except:
                    diagram_plan = self._create_fallback_diagram_plan(diagram_type, specification)
            
            # Generate the actual diagram
            if self.graphics_enabled and MATPLOTLIB_AVAILABLE:
                diagram_file = await self._create_matplotlib_diagram(diagram_plan, diagram_type)
            else:
                diagram_file = await self._create_text_diagram(diagram_plan, diagram_type)
            
            generation_time = time.time() - start_time
            
            result = {
                "success": True,
                "diagram_type": diagram_type,
                "file_path": str(diagram_file),
                "plan": diagram_plan,
                "generation_time": f"{generation_time:.3f}s",
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Diagram generated: {diagram_file}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Diagram generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "diagram_type": diagram_type
            }
    
    def _create_fallback_diagram_plan(self, diagram_type: str, specification: str) -> Dict[str, Any]:
        """Create a structured diagram plan when AI is not available"""
        
        if diagram_type.lower() == "architecture":
            return {
                "title": f"System Architecture: {specification[:50]}...",
                "components": [
                    {"name": "Frontend", "type": "frontend", "x": 1, "y": 1},
                    {"name": "API Gateway", "type": "middleware", "x": 2, "y": 1},
                    {"name": "Backend", "type": "backend", "x": 3, "y": 1},
                    {"name": "Database", "type": "storage", "x": 3, "y": 2}
                ],
                "connections": [
                    {"from": "Frontend", "to": "API Gateway"},
                    {"from": "API Gateway", "to": "Backend"},
                    {"from": "Backend", "to": "Database"}
                ],
                "layout": "hierarchical",
                "styling": {"primary": "#2E86AB", "secondary": "#A23B72", "accent": "#F18F01"}
            }
        
        elif diagram_type.lower() == "flowchart":
            return {
                "title": f"Process Flow: {specification[:50]}...",
                "components": [
                    {"name": "Start", "type": "start", "x": 1, "y": 1},
                    {"name": "Input", "type": "process", "x": 2, "y": 1},
                    {"name": "Decision", "type": "decision", "x": 3, "y": 1},
                    {"name": "Action", "type": "process", "x": 4, "y": 1},
                    {"name": "End", "type": "end", "x": 5, "y": 1}
                ],
                "connections": [
                    {"from": "Start", "to": "Input"},
                    {"from": "Input", "to": "Decision"},
                    {"from": "Decision", "to": "Action"},
                    {"from": "Action", "to": "End"}
                ],
                "layout": "flow",
                "styling": {"primary": "#4CAF50", "secondary": "#FF9800", "accent": "#2196F3"}
            }
        
        else:  # Generic network diagram
            return {
                "title": f"{diagram_type.title()}: {specification[:50]}...",
                "components": [
                    {"name": "Node A", "type": "node", "x": 1, "y": 1},
                    {"name": "Node B", "type": "node", "x": 2, "y": 2},
                    {"name": "Node C", "type": "node", "x": 3, "y": 1}
                ],
                "connections": [
                    {"from": "Node A", "to": "Node B"},
                    {"from": "Node B", "to": "Node C"}
                ],
                "layout": "network",
                "styling": {"primary": "#6366f1", "secondary": "#ec4899", "accent": "#10b981"}
            }
    
    async def _create_matplotlib_diagram(self, plan: Dict[str, Any], diagram_type: str) -> Path:
        """Create diagram using Matplotlib"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            
            # Create figure
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            ax.set_xlim(0, 6)
            ax.set_ylim(0, 4)
            ax.set_aspect('equal')
            
            # Set title
            plt.title(plan["title"], fontsize=16, fontweight='bold', pad=20)
            
            # Color scheme
            colors = plan["styling"]
            
            # Draw components
            for component in plan["components"]:
                x, y = component.get("x", 1), component.get("y", 1)
                
                # Determine shape and color based on type
                node_style = self._get_node_style(component.get("type", "default"))
                
                if component.get("type") == "decision":
                    # Diamond shape for decisions
                    diamond = patches.RegularPolygon((x, y), 4, radius=0.3, 
                                                   orientation=3.14159/4, 
                                                   facecolor=node_style["color"], 
                                                   edgecolor='black')
                    ax.add_patch(diamond)
                elif component.get("type") in ["start", "end"]:
                    # Oval shape for start/end
                    oval = patches.Ellipse((x, y), 0.6, 0.3, 
                                         facecolor=node_style["color"], 
                                         edgecolor='black')
                    ax.add_patch(oval)
                else:
                    # Rectangle for other components
                    rect = patches.Rectangle((x-0.3, y-0.2), 0.6, 0.4, 
                                           facecolor=node_style["color"], 
                                           edgecolor='black')
                    ax.add_patch(rect)
                
                # Add text
                ax.text(x, y, component["name"], ha='center', va='center', 
                       fontsize=10, fontweight='bold', color='white')
            
            # Draw connections
            for connection in plan["connections"]:
                from_comp = next(c for c in plan["components"] if c["name"] == connection["from"])
                to_comp = next(c for c in plan["components"] if c["name"] == connection["to"])
                
                x1, y1 = from_comp.get("x", 1), from_comp.get("y", 1)
                x2, y2 = to_comp.get("x", 1), to_comp.get("y", 1)
                
                # Draw arrow
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=2, color=colors["secondary"]))
            
            # Remove axes
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            # Save diagram
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{diagram_type}_{timestamp}.png"
            output_file = self.output_dir / filename
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"❌ Matplotlib diagram creation failed: {e}")
            # Fallback to text diagram
            return await self._create_text_diagram(plan, diagram_type)
    
    async def _create_text_diagram(self, plan: Dict[str, Any], diagram_type: str) -> Path:
        """Create text-based diagram when graphics not available"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{diagram_type}_{timestamp}.txt"
            output_file = self.output_dir / filename
            
            # Create text representation
            content = f"""
╔══════════════════════════════════════════════════════════════╗
║                     {plan['title'][:54]}                      ║
╚══════════════════════════════════════════════════════════════╝

🏗️ COMPONENTS:
{'─' * 60}
"""
            
            for i, component in enumerate(plan["components"], 1):
                comp_type = component.get('type', 'default')
                icon = self._get_component_icon(comp_type)
                content += f"{i:2d}. {icon} {component['name']} ({comp_type})\n"
            
            content += f"""
🔗 CONNECTIONS:
{'─' * 60}
"""
            
            for connection in plan["connections"]:
                content += f"   {connection['from']} ──→ {connection['to']}\n"
            
            content += f"""
🎨 LAYOUT: {plan['layout']}
⏰ GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 TYPE: {diagram_type.upper()}

{'═' * 66}
Generated by Rudh Creative Engine V4.1
Advanced AI-Powered Content Creation
{'═' * 66}
"""
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"❌ Text diagram creation failed: {e}")
            raise
    
    def _get_component_icon(self, comp_type: str) -> str:
        """Get icon for component type"""
        icons = {
            "start": "🟢",
            "end": "🔴",
            "process": "📦",
            "decision": "💎",
            "frontend": "💻",
            "backend": "⚙️",
            "database": "🗄️",
            "storage": "💾",
            "middleware": "🔧",
            "network": "🌐",
            "default": "📋"
        }
        return icons.get(comp_type, icons["default"])
    
    def _get_node_style(self, node_type: str) -> Dict[str, str]:
        """Get visual styling for different node types"""
        styles = {
            "start": {"shape": "ellipse", "color": "#4CAF50"},
            "end": {"shape": "ellipse", "color": "#F44336"},
            "process": {"shape": "box", "color": "#2196F3"},
            "decision": {"shape": "diamond", "color": "#FF9800"},
            "frontend": {"shape": "box", "color": "#9C27B0"},
            "backend": {"shape": "box", "color": "#3F51B5"},
            "database": {"shape": "cylinder", "color": "#795548"},
            "storage": {"shape": "folder", "color": "#607D8B"},
            "middleware": {"shape": "hexagon", "color": "#009688"},
            "network": {"shape": "circle", "color": "#00BCD4"},
            "default": {"shape": "box", "color": "#6366f1"}
        }
        
        return styles.get(node_type, styles["default"])
    
    async def generate_business_content(self, content_type: str, specification: str) -> Dict[str, Any]:
        """Generate business content (presentations, reports, etc.)"""
        try:
            start_time = time.time()
            
            self.logger.info(f"📋 Generating {content_type} content...")
            
            # AI-powered content creation
            ai_prompt = f"""
            You are a professional business content creator. Create structured content for:
            
            Content Type: {content_type}
            Specification: {specification}
            
            Create a detailed {content_type} with:
            - Professional title
            - Clear section structure
            - Key points and insights
            - Actionable recommendations
            - Chennai business context where relevant
            
            Make it professional and comprehensive.
            """
            
            ai_response = await self.ai_service.get_response(ai_prompt)
            
            # Create fallback content if AI not available
            if "AI service not available" in ai_response:
                ai_response = self._create_fallback_content(content_type, specification)
            
            # Create content file
            content_file = await self._create_content_file(content_type, ai_response, specification)
            
            generation_time = time.time() - start_time
            
            result = {
                "success": True,
                "content_type": content_type,
                "file_path": str(content_file),
                "content_preview": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
                "generation_time": f"{generation_time:.3f}s",
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Content generated: {content_file}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Content generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "content_type": content_type
            }
    
    def _create_fallback_content(self, content_type: str, specification: str) -> str:
        """Create fallback content when AI is not available"""
        
        if content_type.lower() == "presentation":
            return f"""# {specification}

## Executive Summary
Professional presentation overview for {specification}.

## Key Objectives
- Define clear goals and outcomes
- Present actionable solutions
- Demonstrate business value
- Outline implementation approach

## Current Situation
- Market analysis and context
- Key challenges and opportunities
- Stakeholder requirements

## Proposed Solution
- Technical approach and methodology
- Resource requirements and timeline
- Risk mitigation strategies
- Expected outcomes and benefits

## Implementation Plan
- Phase 1: Planning and preparation
- Phase 2: Development and testing
- Phase 3: Deployment and monitoring
- Phase 4: Optimization and scaling

## Business Impact
- Cost savings and efficiency gains
- Revenue opportunities
- Competitive advantages
- Long-term strategic value

## Next Steps
- Immediate action items
- Decision points and approvals
- Timeline and milestones
- Success metrics and KPIs

## Conclusion
Summary of key points and call to action for stakeholders.
"""
        
        elif content_type.lower() == "report":
            return f"""# Technical Report: {specification}

## Abstract
Comprehensive analysis and documentation for {specification}.

## Introduction
Background information and context for this technical report.

## Methodology
- Research approach and data collection
- Analysis techniques and tools
- Quality assurance processes

## Findings
- Key discoveries and insights
- Data analysis results
- Technical specifications

## Analysis
- Detailed examination of findings
- Comparative analysis
- Trend identification

## Recommendations
- Technical recommendations
- Best practices
- Implementation guidelines

## Conclusion
Summary of findings and recommended actions.

## References
- Technical documentation
- Industry standards
- Research sources
"""
        
        else:  # Generic business content
            return f"""# {content_type.title()}: {specification}

## Overview
Professional {content_type} document for {specification}.

## Key Points
- Strategic objectives and goals
- Current market situation
- Proposed solutions and approaches
- Expected outcomes and benefits

## Details
Comprehensive information and analysis relevant to {specification}.

## Recommendations
- Actionable next steps
- Implementation guidelines
- Success metrics

## Conclusion
Summary and call to action.
"""
    
    async def _create_content_file(self, content_type: str, content: str, specification: str) -> Path:
        """Create content file with proper formatting"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{content_type}_{timestamp}.md"
            output_file = self.output_dir / filename
            
            # Format content with header
            formatted_content = f"""---
title: {content_type.title()} Document
specification: {specification}
generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
type: {content_type}
---

{content}

---

**Generated by:** Rudh Creative Engine V4.1  
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Type:** {content_type.title()}  
**Context:** Chennai Business Intelligence & Content Creation  
"""
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"❌ Content file creation failed: {e}")
            raise
    
    async def list_templates(self) -> List[Dict[str, Any]]:
        """List available creative templates"""
        templates = []
        
        # Built-in template categories
        template_categories = {
            "📊 Technical Diagrams": [
                {"name": "System Architecture", "type": "architecture", "description": "Cloud and system architecture diagrams"},
                {"name": "Process Flow", "type": "flowchart", "description": "Business and technical process flows"},
                {"name": "Network Diagram", "type": "network", "description": "Network topology and connections"},
                {"name": "Database Schema", "type": "database", "description": "Database relationships and structure"}
            ],
            "📋 Business Content": [
                {"name": "Business Presentation", "type": "presentation", "description": "Professional business presentations"},
                {"name": "Technical Report", "type": "report", "description": "Detailed technical documentation"},
                {"name": "Project Proposal", "type": "proposal", "description": "Project and business proposals"},
                {"name": "Marketing Material", "type": "marketing", "description": "Marketing content and materials"}
            ]
        }
        
        for category, items in template_categories.items():
            for item in items:
                templates.append({
                    "category": category,
                    "name": item["name"],
                    "type": item["type"],
                    "description": item["description"],
                    "available": True
                })
        
        return templates
    
    async def get_creative_stats(self) -> Dict[str, Any]:
        """Get creative engine statistics"""
        try:
            output_files = list(self.output_dir.glob("*"))
            
            stats = {
                "total_created": len(output_files),
                "graphics_enabled": self.graphics_enabled,
                "matplotlib_available": MATPLOTLIB_AVAILABLE,
                "pil_available": PIL_AVAILABLE,
                "ai_service_status": "connected" if hasattr(self.ai_service, 'client') else "fallback",
                "templates_available": len(await self.list_templates()),
                "output_directory": str(self.output_dir),
                "recent_files": [f.name for f in sorted(output_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]]
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Stats generation failed: {e}")
            return {"error": str(e)}


# Test functionality
async def test_creative_engine():
    """Test the creative engine functionality"""
    print("🧪 Testing Rudh Creative Engine V4.1 - FIXED VERSION")
    print("=" * 60)
    
    engine = CreativeEngine()
    
    # Test 1: Technical diagram generation
    print("\n📊 Testing technical diagram generation...")
    diagram_result = await engine.generate_technical_diagram(
        "architecture", 
        "Azure-based AI system with OpenAI, Speech Services, and database"
    )
    print(f"✅ Diagram result: {diagram_result['success']}")
    if diagram_result['success']:
        print(f"📁 File: {diagram_result['file_path']}")
        print(f"⚡ Time: {diagram_result['generation_time']}")
    else:
        print(f"❌ Error: {diagram_result.get('error')}")
    
    # Test 2: Business content generation
    print("\n📋 Testing business content generation...")
    content_result = await engine.generate_business_content(
        "presentation",
        "AI portfolio management system for Chennai market"
    )
    print(f"✅ Content result: {content_result['success']}")
    if content_result['success']:
        print(f"📁 File: {content_result['file_path']}")
        print(f"⚡ Time: {content_result['generation_time']}")
        print(f"📖 Preview: {content_result['content_preview']}")
    else:
        print(f"❌ Error: {content_result.get('error')}")
    
    # Test 3: Templates and stats
    print("\n📚 Testing templates and statistics...")
    templates = await engine.list_templates()
    print(f"✅ Templates available: {len(templates)}")
    for template in templates[:3]:  # Show first 3
        print(f"   • {template['name']} ({template['type']})")
    
    stats = await engine.get_creative_stats()
    print(f"✅ Creative stats:")
    print(f"   📊 Graphics: {'✅' if stats['graphics_enabled'] else '❌'}")
    print(f"   🎨 Matplotlib: {'✅' if stats['matplotlib_available'] else '❌'}")
    print(f"   🖼️ PIL: {'✅' if stats['pil_available'] else '❌'}")
    print(f"   🤖 AI: {stats['ai_service_status']}")
    print(f"   📁 Files created: {stats['total_created']}")
    
    print("\n🎉 Creative Engine testing complete!")
    print("🚀 Ready to create amazing content!")


if __name__ == "__main__":
    print("🚀 Initializing Rudh Creative Engine V4.1 - FIXED VERSION...")
    asyncio.run(test_creative_engine())