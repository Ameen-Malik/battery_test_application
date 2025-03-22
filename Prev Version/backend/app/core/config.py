"""
Configuration module for the backend application.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def getenv_boolean(var_name: str, default_value: bool = False) -> bool:
    """
    Parse a boolean value from environment variable.
    
    Args:
        var_name: Name of the environment variable
        default_value: Default value if the environment variable is not set
        
    Returns:
        Parsed boolean value
    """
    result = os.getenv(var_name, str(default_value)).lower()
    return result in ("1", "true", "t", "yes", "y", "on")


class Settings:
    """
    Application settings class.
    """
    # API
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Battery Test Application")
    
    # CORS Configuration (hardcoded to avoid parsing issues)
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",  # Streamlit default
        "http://127.0.0.1:8501",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Monitoring
    ENABLE_METRICS: bool = getenv_boolean("ENABLE_METRICS", True)


# Create global settings instance
settings = Settings()