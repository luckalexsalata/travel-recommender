import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models import TravelRequest
from app.core.config import settings
from app.api.routes import recommendations_router
from app.core.middleware import LoggingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Travel Recommender API",
    description="API for generating travel recommendations using OpenAI",
    version="1.0.0"
)

# Add middleware
app.add_middleware(LoggingMiddleware)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(
    recommendations_router, 
    prefix="/api/v1/recommendations", 
    tags=["recommendations"]
)

@app.on_event("startup")
async def startup():
    """Initialize application on startup"""
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(TravelRequest.metadata.create_all)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Travel Recommender API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 