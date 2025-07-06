import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"🚀 Starting server on {settings.host}:{settings.port}")
    print(f"📊 Database: {settings.database_url}")
    print(f"🤖 OpenAI Model: {settings.openai_model}")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    ) 