# app/api/schemas/recipes.py
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from .base import BaseResponse, PaginatedResponse, ErrorResponse
from enum import Enum

# Enums used in requests/responses
class MealType(str, Enum):
    BREAKFAST = "breakfast"
    BRUNCH = "brunch"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"

class CookingStyle(str, Enum):
    QUICK_AND_EASY = "quick-and-easy"
    WEEKNIGHT = "weeknight"
    WEEKEND = "weekend"
    SPECIAL_OCCASION = "special-occasion"
    MEAL_PREP = "meal-prep"
    DATE_NIGHT = "date-night"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

# Request/Response Models
class RecipeIngredient(BaseModel):
    item: str
    amount: float
    unit: str
    notes: Optional[str] = None

class RecipeInstruction(BaseModel):
    step_number: int
    content: str
    timing: Optional[str] = None

class RecipeMetadata(BaseModel):
    prep_time: int
    cook_time: int
    total_time: int
    difficulty_level: DifficultyLevel
    cuisine_type: List[str]
    meal_type: MealType
    servings: int
    is_spicy: bool = False

class IngredientSchema(BaseModel):
    item: str = Field(..., description="Name of the ingredient")
    amount: Decimal = Field(..., gt=0, description="Amount of ingredient")
    unit: str = Field(..., description="Unit of measurement")
    notes: Optional[str] = None
    category: Optional[str] = None
    is_optional: bool = False

    @field_validator('amount')
    @classmethod
    def round_amount(cls, v):
        return round(v, 2)

    class Config:
        json_schema_extra = {
            "example": {
                "item": "chicken breast",
                "amount": 500,
                "unit": "g",
                "notes": "skinless",
                "category": "protein",
                "is_optional": False
            }
        }

class InstructionSchema(BaseModel):
    step_number: int = Field(..., gt=0)
    content: str = Field(..., min_length=10)
    timing: Optional[str] = None
    equipment_needed: Optional[List[str]] = None
    temperature: Optional[Dict[str, Any]] = None  # For oven temp, etc
    tips: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "step_number": 1,
                "content": "Preheat the oven to 180°C (350°F)",
                "timing": "5 minutes",
                "equipment_needed": ["oven"],
                "temperature": {
                    "celsius": 180,
                    "fahrenheit": 350
                }
            }
        }

# Update Recipe schema to use the new schemas
class Recipe(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    prep_time: int
    cook_time: int
    total_time: int
    servings: int
    cuisine_type: List[str]
    meal_type: Optional[str]
    cooking_style: Optional[str]
    is_spicy: bool
    ingredients: List[IngredientSchema]
    instructions: List[InstructionSchema]
    equipment_needed: List[str]
    nutritional_info: dict
    dietary_info: dict
    recipe_tips: Optional[List[str]]
    storage_instructions: Optional[str]
    leftover_ideas: Optional[List[str]]

    class Config:
        from_attributes = True

    @classmethod
    def from_db_model(cls, db_recipe: "Recipe") -> "Recipe":
        """Convert from DB model to Pydantic schema"""
        # Convert ingredients from JSON to IngredientSchema
        ingredients = [
            IngredientSchema(**ing) 
            for ing in db_recipe.ingredients
        ]
        
        # Convert instructions from JSON to InstructionSchema
        instructions = [
            InstructionSchema(**inst) 
            for inst in db_recipe.instructions
        ]
        
        # Create Recipe instance with converted data
        return cls(
            id=db_recipe.id,
            title=db_recipe.title,
            description=db_recipe.description,
            prep_time=db_recipe.prep_time,
            cook_time=db_recipe.cook_time,
            total_time=db_recipe.total_time,
            servings=db_recipe.servings,
            cuisine_type=db_recipe.cuisine_type,
            meal_type=db_recipe.meal_type,
            cooking_style=db_recipe.cooking_style,
            is_spicy=db_recipe.is_spicy,
            ingredients=ingredients,
            instructions=instructions,
            equipment_needed=db_recipe.equipment_needed,
            nutritional_info=db_recipe.nutritional_info,
            dietary_info=db_recipe.dietary_info,
            recipe_tips=db_recipe.recipe_tips,
            storage_instructions=db_recipe.storage_instructions,
            leftover_ideas=db_recipe.leftover_ideas
        )

    def to_db_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for DB storage"""
        return {
            "title": self.title,
            "description": self.description,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "total_time": self.total_time,
            "servings": self.servings,
            "cuisine_type": self.cuisine_type,
            "meal_type": self.meal_type,
            "cooking_style": self.cooking_style,
            "is_spicy": self.is_spicy,
            "ingredients": [ing.model_dump() for ing in self.ingredients],
            "instructions": [inst.model_dump() for inst in self.instructions],
            "equipment_needed": self.equipment_needed,
            "nutritional_info": self.nutritional_info,
            "dietary_info": self.dietary_info,
            "recipe_tips": self.recipe_tips,
            "storage_instructions": self.storage_instructions,
            "leftover_ideas": self.leftover_ideas
        }

class RecipeGenerationRequest(BaseModel):
    recipe_type: str = Field(..., description="Type of recipe to generate")
    ingredients: List[str] = Field(default_factory=list)
    meal_type: Optional[str] = None
    cuisine_type: Optional[str] = None
    dietary_restrictions: List[str] = Field(default_factory=list)
    servings: int = Field(default=2, ge=1, le=12)
    cooking_style: Optional[str] = None
    max_time: Optional[int] = Field(None, ge=0, le=240)
    is_spicy: bool = False
    notes: Optional[str] = None


class RecipeResponse(BaseResponse):
    data: Recipe
    credits_remaining: int
    generation_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))

class RecipeGenerationError(ErrorResponse):
    error_code: str
    error_details: Optional[dict] = None
    retry_after: Optional[int] = None
    credits_remaining: int = 0