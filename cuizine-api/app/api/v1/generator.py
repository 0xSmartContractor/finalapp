from clerk_backend_api import Clerk
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.api.deps import ClerkUser, verify_subscription_access
from app.core.database import get_db
from sqlalchemy.orm import Session
import logging
from typing import Dict, Any

from app.schemas.recipes import (
    RecipeGenerationRequest,
    RecipeResponse,
    RecipeGenerationError
)

# Import from models (DB models)
from app.models.recipes import Recipe as DBRecipe
from app.services.recipe_generator import RecipeGeneratorService

router = APIRouter(prefix="/api/v1/generator", tags=["recipe-generator"])
logger = logging.getLogger(__name__)

@router.post("/generate", 
    response_model=RecipeResponse,  # Use Pydantic schema for response
    responses={
        403: {"model": RecipeGenerationError},
        500: {"model": RecipeGenerationError}
    }
)
async def generate_recipe_endpoint(
    request: RecipeGenerationRequest,  # Use Pydantic schema for request
    background_tasks: BackgroundTasks,
    user: ClerkUser = Depends(verify_subscription_access),
    db: Session = Depends(get_db)
) -> RecipeResponse:
    """Generate a recipe based on user preferences"""
    try:
        # Validate user has remaining recipes
        if user.metadata.recipes_remaining <= 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No recipe credits remaining. Please upgrade your plan."
            )

        # Log generation attempt
        logger.info(f"Generating recipe for user {user.id}", 
                   extra={
                       "user_id": user.id,
                       "recipe_type": request.recipe_type,
                       "ingredients": len(request.ingredients)
                   })

        # Initialize service
        generator_service = RecipeGeneratorService(db)
        
        # Generate recipe
        recipe = await generator_service.generate_recipe(request, user.id)

        # Update user's recipe count in background
        background_tasks.add_task(
            update_user_recipe_count,
            user.id
        )

        return RecipeResponse(
            success=True,
            data=recipe,
            credits_remaining=user.metadata.recipes_remaining - 1,
            generation_id=recipe.id
        )

    except Exception as e:
        logger.error(f"Recipe generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recipe"
        )

@router.post("/regenerate/{recipe_id}", 
    response_model=RecipeResponse,
    responses={
        404: {"model": RecipeGenerationError},
        500: {"model": RecipeGenerationError}
    }
)
async def regenerate_recipe(
    recipe_id: str,
    background_tasks: BackgroundTasks,
    user: ClerkUser = Depends(verify_subscription_access),
    db: Session = Depends(get_db)
) -> RecipeResponse:
    """Regenerate a recipe with the same parameters"""
    try:
        generator_service = RecipeGeneratorService(db)
        
        # Get original recipe parameters
        original_params = await generator_service.get_recipe_parameters(recipe_id)
        if not original_params:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Original recipe not found"
            )

        # Create new request from original parameters
        request = RecipeGenerationRequest(**original_params)
        
        # Generate new recipe
        recipe = await generator_service.generate_recipe(request, user.id)
        
        # Update user's recipe count in background
        background_tasks.add_task(
            update_user_recipe_count,
            user.id
        )
        
        return RecipeResponse(
            success=True,
            data=recipe,
            credits_remaining=user.metadata.recipes_remaining - 1,
            generation_id=recipe.id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recipe regeneration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to regenerate recipe"
        )

async def update_user_recipe_count(user_id: str) -> None:
    """Update user's remaining recipe count"""
    try:
        # Get current metadata
        user = Clerk.users.get(user_id=user_id)
        metadata = user.public_metadata or {}
        
        # Update recipe count
        recipes_remaining = metadata.get('recipes_remaining', 0) - 1
        recipes_generated = metadata.get('recipes_generated', 0) + 1
        
        # Update metadata
        Clerk.users.update_metadata(
            user_id=user_id,
            public_metadata={
                **metadata,
                'recipes_remaining': max(0, recipes_remaining),
                'recipes_generated': recipes_generated
            }
        )
    except Exception as e:
        logger.error(f"Failed to update recipe count: {str(e)}")
        raise

@router.get("/credits")
async def get_recipe_credits(
    user: ClerkUser = Depends(verify_subscription_access)
) -> Dict[str, Any]:
    """Get user's remaining recipe credits"""
    return {
        "success": True,
        "data": {
            "remaining": user.metadata.recipes_remaining,
            "total": get_plan_limit(user.metadata.subscription_tier),
            "subscription_tier": user.metadata.subscription_tier
        }
    }

def get_plan_limit(tier: str) -> int:
    """Get recipe limit for subscription tier"""
    limits = {
        'free': 5,
        'pro': 100,
        'premium': 100
    }
    return limits.get(tier, 5)