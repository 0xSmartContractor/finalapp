from pydantic import BaseModel
from typing import List, Optional
from app.models.recipes import Recipe, RecipeMetadata

class APIResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    
class RecipeResponse(APIResponse):
    data: Recipe

class RecipeListResponse(APIResponse):
    data: List[Recipe]
    total: int
    page: int
    per_page: int
    
class RecipeGenerationResponse(APIResponse):
    data: Recipe
    generation_id: str  # For tracking/retry purposes
    credits_remaining: int