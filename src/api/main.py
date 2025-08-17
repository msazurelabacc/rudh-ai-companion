"""
FastAPI application for Rudh AI Companion
Provides REST API endpoints to interact with Rudh
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rudh_core.core import RudhCore
from config.config import RudhConfig

# Initialize FastAPI app
app = FastAPI(
    title="Rudh AI Companion API",
    description="Advanced AI Companion with Emotional Intelligence",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Rudh instance
rudh_instance: Optional[RudhCore] = None

# Pydantic models for API
class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"
    context: Optional[Dict] = None

class MessageResponse(BaseModel):
    response: str
    emotion_detected: Dict
    strategy_used: str
    timestamp: str
    confidence: float
    language_detected: str
    rudh_mood: str

class HealthResponse(BaseModel):
    status: str
    rudh_initialized: bool
    stats: Dict

class ConversationHistoryResponse(BaseModel):
    conversations: List[Dict]
    total_count: int

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize Rudh on startup"""
    global rudh_instance
    
    logging.info("🚀 Starting Rudh AI Companion API...")
    
    try:
        config = RudhConfig.get_config()
        rudh_instance = RudhCore(config)
        
        # Initialize Rudh
        success = await rudh_instance.initialize()
        
        if success:
            logging.info("✅ Rudh AI Companion API started successfully!")
        else:
            logging.warning("⚠️ Rudh started with limited functionality")
            
    except Exception as e:
        logging.error(f"❌ Failed to start Rudh: {e}")
        rudh_instance = None

# API Endpoints
@app.get("/", response_model=Dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🤖 Rudh AI Companion API",
        "version": "0.1.0",
        "status": "active",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    global rudh_instance
    
    if not rudh_instance:
        raise HTTPException(status_code=503, detail="Rudh not initialized")
    
    stats = rudh_instance.get_stats()
    
    return HealthResponse(
        status="healthy" if rudh_instance.is_initialized else "degraded",
        rudh_initialized=rudh_instance.is_initialized,
        stats=stats
    )

@app.post("/chat", response_model=MessageResponse)
async def chat_with_rudh(request: MessageRequest):
    """Main chat endpoint to interact with Rudh"""
    global rudh_instance
    
    if not rudh_instance:
        raise HTTPException(status_code=503, detail="Rudh not initialized")
    
    try:
        # Process message with Rudh
        response = await rudh_instance.process_message(
            user_input=request.message,
            user_id=request.user_id
        )
        
        return MessageResponse(
            response=response["response"],
            emotion_detected=response["emotion_detected"],
            strategy_used=response.get("strategy_used", "unknown"),
            timestamp=response["timestamp"],
            confidence=response.get("confidence", 0.0),
            language_detected=response.get("language_detected", "english"),
            rudh_mood=response.get("rudh_mood", "neutral")
        )
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/conversations/{user_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(user_id: str, limit: int = 10):
    """Get conversation history for a user"""
    global rudh_instance
    
    if not rudh_instance:
        raise HTTPException(status_code=503, detail="Rudh not initialized")
    
    try:
        conversations = rudh_instance.get_conversation_history(user_id, limit)
        
        return ConversationHistoryResponse(
            conversations=conversations,
            total_count=len(conversations)
        )
        
    except Exception as e:
        logging.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")

@app.get("/stats", response_model=Dict)
async def get_rudh_stats():
    """Get Rudh's operational statistics"""
    global rudh_instance
    
    if not rudh_instance:
        raise HTTPException(status_code=503, detail="Rudh not initialized")
    
    return rudh_instance.get_stats()

@app.post("/admin/reinitialize")
async def reinitialize_rudh():
    """Admin endpoint to reinitialize Rudh"""
    global rudh_instance
    
    try:
        if rudh_instance:
            success = await rudh_instance.initialize()
            return {"status": "success" if success else "partial", "message": "Rudh reinitialized"}
        else:
            config = RudhConfig.get_config()
            rudh_instance = RudhCore(config)
            success = await rudh_instance.initialize()
            return {"status": "success" if success else "partial", "message": "Rudh created and initialized"}
            
    except Exception as e:
        logging.error(f"Error reinitializing Rudh: {e}")
        raise HTTPException(status_code=500, detail=f"Reinitialization failed: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "suggestion": "Try /docs for API documentation"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "Rudh encountered an unexpected error"}

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration
    config = RudhConfig.get_config()
    api_config = config["api"]
    
    print("🚀 Starting Rudh AI Companion API server...")
    print(f"📍 Server will be available at: http://{api_config['host']}:{api_config['port']}")
    print(f"📚 API Documentation: http://{api_config['host']}:{api_config['port']}/docs")
    
    uvicorn.run(
        "main:app",
        host=api_config["host"],
        port=api_config["port"],
        reload=api_config["reload"],
        log_level="info"
    )
