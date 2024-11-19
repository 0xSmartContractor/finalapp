from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Your exact environment variables from the .env file
    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    API_SECRET: str
    CLERK_PUB_KEY: str
    CLERK_SECRET_KEY: str
    CLERK_JWKS_URL: str 
    CLERK_ISSUER: str 
    CLERK_AUDIENCE: str 
    OPENAI_API_KEY: str
    REDIS_URL: str = "your_redis_url"  # Optional with default
    FRONTEND_URL: str = "your_nextjs_url"  # Optional with default
    SLACK_TOKEN: Optional[str] = "your_slack_token"  # Optional
    SENTRY_DSN: Optional[str] = "your_sentry_dsn"  # Optional
    # Upstash Redis
    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str
    # Rate Limits (requests per minute)
    FREE_RATE_LIMIT: int = 10
    PRO_RATE_LIMIT: int = 50
    PREMIUM_RATE_LIMIT: int = 100
    
    

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()