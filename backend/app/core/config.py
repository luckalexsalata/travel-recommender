from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from typing import List

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    openai_model: str = "gpt-3.5-turbo-1106"
    
    # Database Configuration
    database_url: str = Field(alias="DATABASE_URL")
    
    # Server Configuration
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    
    # CORS Configuration
    cors_origins: List[str] = ["*"]  # In production, specify specific domains
    
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env"
    )

settings = Settings() 