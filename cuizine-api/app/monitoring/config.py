from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict

class MonitoringSettings(BaseSettings):
    CLERK_SECRET_KEY: str
    SLACK_TOKEN: str | None = None
    SENTRY_DSN: str | None = None
    RECIPE_LIMITS: Dict[str, int] = {
        "free": 5,
        "pro": 100,
        "premium": 100
    }
    MONITORING_PORT: int = 8000
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_monitoring_settings() -> MonitoringSettings:
    return MonitoringSettings()