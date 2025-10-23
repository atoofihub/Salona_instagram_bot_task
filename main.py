"""
Main API service - Instagram Direct Message simulator with RAG and LLM
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from typing import Optional
import uvicorn

from config import API_HOST, API_PORT, MAX_MESSAGE_LENGTH, RATE_LIMIT
from database import Database
from rag_service import RAGService
from llm_service import LLMService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG and LLM Response Bot",
    description="Instagram Direct Message simulator with intelligent product search",
    version="1.0.0"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class DirectMessage(BaseModel):
    """Input message model"""
    sender_id: str = Field(..., description="Sender ID", min_length=1, max_length=100)
    message_id: str = Field(..., description="Message ID", min_length=1, max_length=100)
    text: str = Field(..., description="Message text", min_length=1)
    
    @validator('text')
    def validate_text_length(cls, v):
        if len(v) > MAX_MESSAGE_LENGTH:
            raise ValueError(f'Message length should not exceed {MAX_MESSAGE_LENGTH} characters')
        return v.strip()
    
    @validator('sender_id', 'message_id')
    def validate_ids(cls, v):
        if any(char in v for char in ['<', '>', '"', "'", ';', '--']):
            raise ValueError('ID contains forbidden characters')
        return v


class BotResponse(BaseModel):
    """Output response model"""
    reply: str = Field(..., description="Bot response in Persian")
try:
    db = Database()
    rag_service = RAGService(db)
    llm_service = LLMService()
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    raise


@app.get("/")
async def root():
    return {
        "message": "RAG and LLM Response Bot Service",
        "version": "1.0.0",
        "endpoints": {
            "/simulate_dm": "Send message to bot (POST)",
            "/health": "Health check (GET)",
            "/stats": "Database stats (GET)"
        }
    }


@app.get("/health")
async def health_check():
    try:
        products = db.get_all_products(limit=1)
        return {
            "status": "healthy",
            "database": "connected",
            "llm": "configured"
        }
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.get("/stats")
async def get_stats():
    try:
        products = db.get_all_products(limit=1000)
        return {
            "total_products": len(products),
            "status": "ok"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error getting statistics")


@app.post("/simulate_dm", response_model=BotResponse)
@limiter.limit(RATE_LIMIT)
async def simulate_direct_message(request: Request, message: DirectMessage):
    """Instagram Direct Message simulator"""
    try:
        logger.info(
            f"New message - sender_id: {message.sender_id}, "
            f"message_id: {message.message_id}, text: {message.text}"
        )
        
        retrieved_products = rag_service.retrieve(message.text)
        logger.info(f"Retrieved products count: {len(retrieved_products)}")
        
        bot_reply = llm_service.generate_response(
            user_message=message.text,
            retrieved_products=retrieved_products
        )
        logger.info(f"Generated response: {bot_reply[:100]}...")
        
        return BotResponse(reply=bot_reply)
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Internal server error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing message. Please try again."
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    logger.info(f"Starting service on {API_HOST}:{API_PORT}")
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )

