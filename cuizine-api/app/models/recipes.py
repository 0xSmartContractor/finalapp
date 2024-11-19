from sqlalchemy import Column, String, Integer, JSON, Boolean, ARRAY, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    difficulty_level = Column(String)
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    total_time = Column(Integer)
    servings = Column(Integer)
    cuisine_type = Column(ARRAY(String))
    meal_type = Column(String)
    cooking_style = Column(String)  # homestyle, gourmet, etc
    preparation_method = Column(String)  # grilled, baked, etc
    is_spicy = Column(Boolean, default=False)
    
    # Recipe components
    ingredients = Column(JSON)  # List of {amount, unit, item, notes}
    instructions = Column(JSON)  # List of {step_number, content, timing}
    equipment_needed = Column(JSON)
    
    # Additional info
    nutritional_info = Column(JSON)
    dietary_info = Column(JSON)  # vegetarian, vegan, etc
    recipe_tips = Column(JSON)
    storage_instructions = Column(String)
    scaling_notes = Column(String)
    leftover_ideas = Column(ARRAY(String))
    
    # Metadata
    source_type = Column(String)  # 'user', 'ai', 'admin'
    generated_from = Column(JSON)  # Store original generation parameters
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Stats
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)

class UserRecipeInteraction(Base):
    __tablename__ = "user_recipe_interactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    recipe_id = Column(String, ForeignKey('recipes.id'))
    interaction_type = Column(String)  # 'view', 'like', 'save', 'generate'
    created_at = Column(DateTime(timezone=True), server_default=func.now())