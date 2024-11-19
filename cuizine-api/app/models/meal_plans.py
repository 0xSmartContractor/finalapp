# app/models/meal_plans.py
from sqlalchemy import Column, String, Integer, JSON, Boolean, ARRAY, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum

class PreferenceLevel(enum.Enum):
    MUST_HAVE = "must_have"
    PREFERRED = "preferred"
    NEUTRAL = "neutral"
    AVOID = "avoid"
    NEVER = "never"

class BudgetLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class MealPlanPreferences(Base):
    __tablename__ = "meal_plan_preferences"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    
    # Basic Preferences
    dietary_restrictions = Column(ARRAY(String))
    allergies = Column(ARRAY(String))
    cooking_skill_level = Column(String)
    serving_size = Column(Integer)
    
    # Time & Budget
    budget_level = Column(Enum(BudgetLevel))
    weekday_max_prep = Column(Integer)
    weekend_max_prep = Column(Integer)
    
    # Meal Preferences
    breakfast_included = Column(Boolean, default=True)
    meal_preferences = Column(JSON)  # Structured preferences for each meal type
    cuisine_preferences = Column(JSON)  # Weighted preferences for cuisines
    
    ingredient_optimization = Column(Boolean, default=True)
    max_ingredient_repeat_days = Column(Integer, default=3)  # How many days to use an ingredient
    preferred_leftover_usage = Column(JSON, default={
        "enabled": True,
        "max_days": 2,  # How long leftovers can be used
        "preferred_ingredients": []  # Ingredients good for reuse
    })

    # Nutritional Targets
    nutritional_targets = Column(JSON)
    
    # Shopping & Prep
    shopping_frequency = Column(String)
    meal_prep_friendly = Column(Boolean, default=False)
    leftovers_enabled = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Weekly Stats
    total_calories = Column(Integer)
    total_cost = Column(Float)
    unique_ingredients = Column(Integer)
    prep_time_required = Column(Integer)  # Total minutes
    
    # Status
    is_active = Column(Boolean, default=True)
    is_generated = Column(Boolean, default=False)
    generation_status = Column(String)  # For tracking long-running generations
    
    # Relationships
    days = relationship("MealPlanDay", back_populates="meal_plan")
    shopping_lists = relationship("ShoppingList", back_populates="meal_plan")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MealPlanDay(Base):
    __tablename__ = "meal_plan_days"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meal_plan_id = Column(String, ForeignKey('meal_plans.id'))
    date = Column(DateTime(timezone=True), nullable=False)
    
    # Daily Stats
    total_calories = Column(Integer)
    total_prep_time = Column(Integer)
    
    
    # Meals
    breakfast = Column(JSON)  # References to recipes with modifications
    lunch = Column(JSON)
    dinner = Column(JSON)
    snacks = Column(JSON, nullable=True)
    leftover_ingredients = Column(JSON)  # Track ingredients that will have leftovers
    planned_leftover_usage = Column(JSON)  # Track where leftovers will be used
    ingredient_inventory = Column(JSON)  # Track what ingredients are available this day
    
    # Prep Instructions
    prep_instructions = Column(JSON)  # Timing and steps for the day
    
    meal_plan = relationship("MealPlan", back_populates="days")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class IngredientUsage(Base):
    __tablename__ = "ingredient_usage"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meal_plan_id = Column(String, ForeignKey('meal_plans.id'))
    ingredient_name = Column(String)
    total_amount = Column(Float)
    unit = Column(String)
    
    # Track where this ingredient is used
    usage_schedule = Column(JSON)  # {"day_1": {"amount": 200, "meal": "dinner"}, ...}
    leftover_amounts = Column(JSON)  # {"day_1": 150, "day_2": 100, ...}
    recipes_used = Column(ARRAY(String))  # Recipe IDs using this ingredient

class IngredientInventory(Base):
   __tablename__ = "ingredient_inventory"
   
   id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
   meal_plan_id = Column(String, ForeignKey('meal_plans.id'))
   date = Column(DateTime(timezone=True))
   ingredients = Column(JSON) # {name: {amount, unit, expiry, source_recipe}}
   planned_usage = Column(JSON) # {recipe_id: {ingredient: amount}}