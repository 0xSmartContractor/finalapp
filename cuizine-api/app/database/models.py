from sqlalchemy import Column, String, Integer, JSON, Boolean, ARRAY, DateTime, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from .session import Base

def generate_uuid():
    return str(uuid.uuid4())

# Association tables
recipe_tags = Table(
    'recipe_tags',
    Base.metadata,
    Column('recipe_id', String, ForeignKey('recipes.id')),
    Column('tag_id', String, ForeignKey('tags.id'))
)

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(String)
    difficulty_level = Column(String)
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    total_time = Column(Integer)
    servings = Column(Integer)
    cuisine_type = Column(ARRAY(String))
    meal_type = Column(String)
    cooking_style = Column(String)
    preparation_method = Column(String)
    is_spicy = Column(Boolean, default=False)
    
    # Recipe components
    ingredients = Column(JSONB)  # List of {amount, unit, item, notes}
    instructions = Column(JSONB)  # List of {step_number, content, timing}
    equipment_needed = Column(JSONB)
    
    # Additional info
    nutritional_info = Column(JSONB)
    dietary_info = Column(JSONB)  # vegetarian, vegan, etc
    recipe_tips = Column(JSONB)
    storage_instructions = Column(String)
    scaling_notes = Column(String)
    leftover_ideas = Column(ARRAY(String))
    
    # Generation info
    source_type = Column(String)  # 'user', 'ai', 'admin'
    generated_from = Column(JSONB)  # Store original generation parameters
    creator_user_id = Column(String)  # Clerk user ID
    
    # Stats and metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)
    
    # Relationships
    tags = relationship("Tag", secondary=recipe_tags, back_populates="recipes")
    photos = relationship("RecipePhoto", back_populates="recipe")
    shopping_lists = relationship("ShoppingList", back_populates="recipe")

class RecipePhoto(Base):
    __tablename__ = "recipe_photos"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    recipe_id = Column(String, ForeignKey('recipes.id'))
    user_id = Column(String, nullable=False)  # Clerk user ID
    photo_url = Column(String, nullable=False)
    caption = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    recipe = relationship("Recipe", back_populates="photos")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    type = Column(String)  # e.g., 'cuisine', 'dietary', 'ingredient'
    
    recipes = relationship("Recipe", secondary=recipe_tags, back_populates="tags")

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)  # Clerk user ID
    recipe_id = Column(String, ForeignKey('recipes.id'), nullable=True)
    name = Column(String)
    items = Column(JSONB)  # List of {name, amount, unit, category, checked}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    recipe = relationship("Recipe", back_populates="shopping_lists")

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    user_id = Column(String, primary_key=True)  # Clerk user ID
    dietary_restrictions = Column(ARRAY(String))
    favorite_cuisines = Column(ARRAY(String))
    disliked_ingredients = Column(ARRAY(String))
    cooking_skill_level = Column(String)
    household_size = Column(Integer)
    preferred_units = Column(String)  # 'metric' or 'imperial'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())