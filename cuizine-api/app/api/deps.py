from fastapi import HTTPException, logger, status
from typing import TypeVar, Type, Optional
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class RateLimitError(Exception):
    def __init__(self, limit: int, reset_time: int):
        self.limit = limit
        self.reset_time = reset_time
        super().__init__(f"Rate limit exceeded. Limit: {limit}")

def handle_clerk_error(error: Exception) -> None:
    """Map Clerk SDK errors to appropriate HTTP responses"""
    if isinstance(error, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error)
        )
    
    error_mapping = {
        'token_expired': status.HTTP_401_UNAUTHORIZED,
        'invalid_token': status.HTTP_401_UNAUTHORIZED,
        'token_not_active': status.HTTP_403_FORBIDDEN,
        'user_not_found': status.HTTP_404_NOT_FOUND,
        'insufficient_permissions': status.HTTP_403_FORBIDDEN
    }
    
    error_type = getattr(error, 'error_code', 'unknown')
    status_code = error_mapping.get(error_type, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    raise HTTPException(
        status_code=status_code,
        detail=str(error)
    )

def validate_response_model(data: dict, model: Type[T]) -> Optional[T]:
    """Validate response data against a Pydantic model"""
    try:
        return model.model_validate(data)
    except ValidationError as e:
        logger.error(f"Response validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response format from authentication service"
        )