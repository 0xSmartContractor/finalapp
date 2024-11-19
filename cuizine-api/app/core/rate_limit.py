from upstash_redis import Redis
from fastapi import Request
from app.core.config import settings
from typing import Optional

redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)

async def check_rate_limit(identifier: str, limit: int, window: int = 60) -> tuple[bool, Optional[int]]:
    """
    Check rate limit for given identifier
    Returns (is_allowed, remaining_requests)
    """
    try:
        key = f"rate:{identifier}"
        # Get current count
        current = await redis.get(key)
        current = int(current) if current else 0
        
        if current >= limit:
            return False, 0
            
        # Increment and set expiry
        await redis.incr(key)
        await redis.expire(key, window)
        
        remaining = limit - (current + 1)
        return True, remaining
        
    except Exception as e:
        print(f"Rate limiting error: {e}")
        # If rate limiting fails, allow the request
        return True, None

async def reset_rate_limit(identifier: str):
    """Reset rate limit counter for testing"""
    try:
        await redis.del_(f"rate:{identifier}")
    except Exception as e:
        print(f"Error resetting rate limit: {e}")