from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.openai_manager import OpenAIManager
from app.models.recipes import Recipe, Tag, UserPreferences
from app.schemas.recipes import ( 
    Recipe as RecipeSchema,
    RecipeGenerationRequest,
    IngredientSchema,
    InstructionSchema
)
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

class RecipeGeneratorService:
    def __init__(self, db: Session):
        self.db = db
        self.openai = OpenAIManager()

    async def generate_recipe(
        self,
        request: RecipeGenerationRequest,
        user_id: str
    ) -> RecipeSchema:
        """Generate a new recipe based on user requirements"""
        try:
            user_prefs = self._get_user_preferences(user_id)
            generation_params = self._prepare_generation_params(request, user_prefs)
            recipe_data = await self.openai.generate_recipe(generation_params)
            
            # Convert raw ingredients and instructions to schemas for validation
            ingredients = [IngredientSchema(**ing) for ing in recipe_data["ingredients"]]
            instructions = [InstructionSchema(**inst) for inst in recipe_data["instructions"]]
            
            # Store validated data
            db_recipe = self._store_recipe(
                {
                    **recipe_data,
                    "ingredients": [ing.dict() for ing in ingredients],
                    "instructions": [inst.dict() for inst in instructions]
                },
                user_id,
                request
            )
            
            # Convert to response schema using new from_db_model method
            return RecipeSchema.from_db_model(db_recipe)
            
        except Exception as e:
            logger.error(f"Recipe generation failed: {str(e)}")
            raise

    # _get_user_preferences and _prepare_generation_params remain the same

    def _store_recipe(
        self,
        recipe_data: Dict[str, Any],
        user_id: str,
        original_request: RecipeGenerationRequest
    ) -> Recipe:
        """Store generated recipe in database"""
        recipe = Recipe(
            id=str(uuid4()),
            title=recipe_data["title"],
            description=recipe_data["description"],
            prep_time=recipe_data["prep_time"],
            cook_time=recipe_data["cook_time"],
            total_time=recipe_data["prep_time"] + recipe_data["cook_time"],
            servings=recipe_data["servings"],
            difficulty_level=recipe_data["difficulty_level"],
            cuisine_type=recipe_data.get("cuisine_type", []),
            meal_type=recipe_data.get("meal_type"),
            cooking_style=original_request.cooking_style,
            is_spicy=original_request.is_spicy,
            ingredients=recipe_data["ingredients"],  # Now validated via IngredientSchema
            instructions=recipe_data["instructions"],  # Now validated via InstructionSchema
            nutritional_info=recipe_data["nutritional_info"],
            equipment_needed=recipe_data.get("equipment_needed", []),
            dietary_info=recipe_data.get("dietary_info", {}),
            recipe_tips=recipe_data.get("recipe_tips", []),
            storage_instructions=recipe_data.get("storage_instructions"),
            leftover_ideas=recipe_data.get("leftover_ideas", []),
            source_type="ai",
            generated_from=original_request.dict(),
            creator_user_id=user_id
        )
        
        self._add_recipe_tags(recipe, recipe_data)
        
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        
        return recipe

    def _add_recipe_tags(self, recipe: Recipe, recipe_data: Dict[str, Any]) -> None:
        """Add tags to recipe"""
        # Method remains the same
        ...

    async def get_recipe(self, recipe_id: str) -> Optional[RecipeSchema]:
        """Get a recipe by ID"""
        try:
            recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
            if not recipe:
                return None
            return RecipeSchema.from_db_model(recipe)
        except Exception as e:
            logger.error(f"Error getting recipe: {e}")
            return None

    def validate_recipe_data(self, recipe_data: Dict[str, Any]) -> None:
        """Validate generated recipe data"""
        required_fields = ['title', 'prep_time', 'cook_time', 'ingredients', 'instructions']
        missing_fields = [field for field in required_fields if field not in recipe_data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate ingredients and instructions using schemas
        try:
            [IngredientSchema(**ing) for ing in recipe_data['ingredients']]
            [InstructionSchema(**inst) for inst in recipe_data['instructions']]
        except Exception as e:
            raise ValueError(f"Invalid recipe data format: {str(e)}")