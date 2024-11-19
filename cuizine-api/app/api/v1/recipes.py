from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

from app.schemas.base import BaseResponse, ErrorResponse

class RecipeType(str, Enum):
    RANDOM = "random"
    CUSTOM = "custom"
    CRAZY = "crazy"

class CookingStyle(str, Enum):
    QUICK_AND_EASY = "quick-and-easy"
    WEEKNIGHT = "weeknight"
    WEEKEND = "weekend"
    SPECIAL_OCCASION = "special-occasion"
    MEAL_PREP = "meal-prep"
    DATE_NIGHT = "date-night"

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    BRUNCH = "brunch"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class IngredientItem(BaseModel):
    id: str
    name: str
    amount: Optional[float] = None
    unit: Optional[str] = None
    category: str
    emoji: str
    isCustom: bool = False

class DietaryRestriction(BaseModel):
    id: str
    label: str
    description: str
    icon: str

class RecipeGeneratorRequest(BaseModel):
    recipe_type: RecipeType
    cooking_style: Optional[CookingStyle] = None
    selected_ingredients: List[str] = Field(default_factory=list)
    meal_type: Optional[str] = None
    cuisine: Optional[str] = None
    dietary_restrictions: List[str] = Field(default_factory=list)
    servings: int = 2
    inspiration: Optional[str] = None
    is_spicy: bool = False
    max_prep_time: Optional[int] = None
    max_cook_time: Optional[int] = None
    preferred_methods: Optional[List[str]] = None
    notes: Optional[str] = None

class RecipeIngredient(BaseModel):
    item: str
    amount: float
    unit: str
    notes: Optional[str] = None

class RecipeStep(BaseModel):
    step: int
    content: str
    timing: Optional[str] = None

class NutritionalInfo(BaseModel):
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None

class RecipeMetadata(BaseModel):
    prep_time: int
    cook_time: int
    total_time: int
    difficulty: DifficultyLevel
    cuisine_type: List[str]
    tags: List[str]
    nutritional_info: NutritionalInfo
    recipe_tips: Dict[str, List[str]]

class Recipe(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    metadata: RecipeMetadata
    ingredients: List[RecipeIngredient]
    instructions: List[RecipeStep]
    servings: int
    equipment_needed: List[str]
    dietary_info: Dict[str, bool]
    storage_instructions: Optional[str] = None
    leftover_ideas: Optional[List[str]] = None
    scaling_notes: Optional[str] = None
