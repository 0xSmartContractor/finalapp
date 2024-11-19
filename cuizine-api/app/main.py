import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.deps import get_current_user, ClerkUser, get_rate_limit
from app.core.rate_limit import check_rate_limit
from app.api.v1 import recipes, generator, shopping
from app.database.session import engine, Base
from contextlib import asynccontextmanager
import time
import sentry_sdk
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Sentry if DSN is provided
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0
    )

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created")
        
        # Initialize OpenAI
        await openai_client.models.list()
        logger.info("OpenAI connection verified")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    try:
        await openai_client.close()
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

app = FastAPI(
    title="Cuizine API",
    description="Recipe generation and management API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        try:
            # Get user from token
            auth = request.headers.get("authorization")
            if not auth or not auth.startswith('Bearer '):
                return await call_next(request)
            
            user = await get_current_user(auth)
            rate_limit = await get_rate_limit(user)
            
            # Check rate limit
            identifier = f"{user.id}:{user.metadata.subscription_tier}"
            is_allowed, remaining = await check_rate_limit(identifier, rate_limit)
            
            if not is_allowed:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "tier": user.metadata.subscription_tier,
                        "limit": rate_limit,
                        "window": "1 minute"
                    }
                )
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(rate_limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(int(time.time() + 60))
            
            return response
            
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail}
            )
        except Exception as e:
            logger.error(f"Rate limiting error: {str(e)}")
            return await call_next(request)
    
    return await call_next(request)

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {exc}", exc_info=True)
    
    error_msg = str(exc) if settings.ENVIRONMENT == "development" else "Internal server error"
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
        
    return JSONResponse(
        status_code=500,
        content={"error": error_msg}
    )

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }

# Include routers
app.include_router(
    recipes.router,
    prefix="/api/v1/recipes",
    tags=["recipes"]
)
app.include_router(
    generator.router,
    prefix="/api/v1/generator",
    tags=["recipe-generator"]
)
app.include_router(
    shopping.router,
    prefix="/api/v1/shopping",
    tags=["shopping-lists"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )