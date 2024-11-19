# app/api/schemas/meal_plans.py
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict
from datetime import datetime, date
from enum import Enum


from app.models.meal_plans import MealPlanDay
from app.models.recipes import Recipe
from .base import BaseResponse

class MealPreference(BaseModel):
    included: bool = True
    preferences: List[str] = Field(default_factory=list)
    excluded: List[str] = Field(default_factory=list)
    time_constraints: Optional[Dict[str, int]] = None

class NutritionalTargets(BaseModel):
    calories_per_day: Optional[int] = None
    protein_grams: Optional[int] = None
    carb_grams: Optional[int] = None
    fat_grams: Optional[int] = None
    specific_goals: List[str] = Field(default_factory=list)

class MealPlanRequest(BaseModel):
    start_date: date
    duration_weeks: int = Field(ge=1, le=4)
    preferences: Dict[str, Any] = None
    regenerate_shopping_list: bool = True

class MealPlanResponse(BaseResponse):
    id: str
    start_date: datetime
    end_date: datetime
    days: List["MealPlanDay"]
    shopping_list_id: Optional[str]
    total_calories: int
    total_cost: float
    prep_time_required: int

class DailyMealsResponse(BaseModel):
    date: datetime
    meals: Dict[str, "Recipe"]
    prep_instructions: List[str]
    total_calories: int
    total_prep_time: int