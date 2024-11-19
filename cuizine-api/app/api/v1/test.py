from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any
from app.api.deps import get_current_user, get_subscription_tier, JWTPayload
import jwt

router = APIRouter()

@router.get("/me")
async def read_user_me(
    current_user: JWTPayload = Depends(get_current_user)
) -> Dict[str, Any]:
    """Test endpoint to verify authentication"""
    return {
        "user_id": current_user.sub,
        "email": current_user.email,
        "metadata": current_user.metadata
    }

@router.get("/tier")
async def get_user_tier(
    tier: str = Depends(get_subscription_tier)
) -> Dict[str, str]:
    """Get user's current subscription tier"""
    return {"tier": tier}

@router.get("/health")
async def test_health() -> Dict[str, str]:
    """Basic health check endpoint"""
    return {"status": "healthy"}

@router.get("/rate-limit-test")
async def test_rate_limit() -> Dict[str, str]:
    """Endpoint to test rate limiting"""
    return {
        "message": "If you see this multiple times quickly, your rate limit hasn't been hit yet!"
    }
@router.get("/verify-token")
async def verify_token(request: Request) -> Dict[str, Any]:
    """Debug endpoint to see JWT token contents"""
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="No authorization header")
        
    try:
        # Remove 'Bearer ' prefix
        token = auth_header.split(' ')[1]
        # Just decode without verification for debugging
        import jwt
        decoded = jwt.decode(token, options={"verify_signature": False})
        return {
            "token_contents": decoded,
            "metadata": decoded.get("metadata", {}),
            "user_id": decoded.get("sub")
        }
    except Exception as e:
        return {"error": str(e)}

# Add test endpoint that doesn't require auth
@router.get("/public")
async def public_test() -> Dict[str, str]:
    """Public endpoint for testing"""
    return {"message": "This is a public endpoint"}

@router.get("/debug-headers")
async def debug_headers(request: Request):
    """Debug endpoint to see what's in the headers"""
    auth_header = request.headers.get("authorization")
    
    try:
        if auth_header:
            # Try to parse the token
            token = auth_header.replace('Bearer ', '')
            decoded = jwt.decode(token, options={"verify_signature": False})
            return {
                "auth_header": auth_header,
                "token": token[:20] + "...",  # Show first 20 chars
                "decoded_token": decoded,
                "all_headers": dict(request.headers)
            }
        else:
            return {
                "error": "No authorization header",
                "all_headers": dict(request.headers)
            }
    except Exception as e:
        return {
            "error": str(e),
            "auth_header": auth_header,
            "all_headers": dict(request.headers)
        }

@router.get("/debug-token")
async def debug_token(request: Request):
    """Debug endpoint to see what's in the token"""
    auth = request.headers.get("authorization")
    if not auth:
        return {"error": "No authorization header"}
        
    try:
        # Handle both with and without 'Bearer ' prefix
        token = auth.replace('Bearer ', '') if 'Bearer ' in auth else auth
        
        # Just decode and show contents
        decoded = jwt.decode(token, options={"verify_signature": False})
        return {
            "token_preview": token[:20] + "...",
            "decoded": decoded,
            "metadata": decoded.get("metadata", {}),
        }
    except Exception as e:
        return {"error": f"Token decode error: {str(e)}"}
    
@router.get("/debug-full")
async def debug_full(request: Request):
    """Debug endpoint to see all relevant info"""
    auth = request.headers.get("authorization")
    
    response = {
        "headers": dict(request.headers),
        "auth_present": bool(auth),
        "client_ip": request.client.host if request.client else "unknown"
    }
    
    if auth:
        try:
            token = auth.replace('Bearer ', '')
            decoded = jwt.decode(token, options={"verify_signature": False})
            response["token_contents"] = decoded
        except Exception as e:
            response["token_error"] = str(e)
            
    return response