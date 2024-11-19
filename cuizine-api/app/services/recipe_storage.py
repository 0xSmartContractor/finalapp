from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.database.models import Recipe, Tag, RecipePhoto
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RecipeStorageService:
    def __init__(self, db: Session):
        self.db = db

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """Get a recipe by ID"""
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()

    def get_user_recipes(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Recipe]:
        """Get recipes for a user with filters"""
        query = self.db.query(Recipe).filter(Recipe.creator_user_id == user_id)
        
        if filters:
            if filters.get('cuisine_type'):
                query = query.filter(Recipe.cuisine_type.contains([filters['cuisine_type']]))
            if filters.get('meal_type'):
                query = query.filter(Recipe.meal_type == filters['meal_type'])
            if filters.get('difficulty_level'):
                query = query.filter(Recipe.difficulty_level == filters['difficulty_level'])
            if filters.get('max_time'):
                query = query.filter(Recipe.total_time <= filters['max_time'])

        return query.order_by(desc(Recipe.created_at)).offset(skip).limit(limit).all()

    def save_recipe(self, recipe: Recipe) -> Recipe:
        """Save or update a recipe"""
        if recipe.id:
            existing = self.get_recipe(recipe.id)
            if existing:
                # Update existing recipe
                for key, value in recipe.__dict__.items():
                    if not key.startswith('_'):
                        setattr(existing, key, value)
                recipe = existing
            
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def add_recipe_photo(
        self,
        recipe_id: str,
        user_id: str,
        photo_url: str,
        caption: Optional[str] = None
    ) -> RecipePhoto:
        """Add a photo to a recipe"""
        photo = RecipePhoto(
            recipe_id=recipe_id,
            user_id=user_id,
            photo_url=photo_url,
            caption=caption
        )
        
        self.db.add(photo)
        self.db.commit()
        self.db.refresh(photo)
        return photo

    def search_recipes(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Recipe]:
        """Search recipes with filters"""
        search = self.db.query(Recipe)
        
        # Add search conditions
        search = search.filter(
            or_(
                Recipe.title.ilike(f"%{query}%"),
                Recipe.description.ilike(f"%{query}%")
            )
        )
        
        if filters:
            # Apply filters
            for key, value in filters.items():
                if hasattr(Recipe, key) and value is not None:
                    search = search.filter(getattr(Recipe, key) == value)
                    
        return search.order_by(desc(Recipe.created_at)).offset(skip).limit(limit).all()

    def get_popular_recipes(
        self,
        limit: int = 10,
        timeframe_days: int = 30
    ) -> List[Recipe]:
        """Get popular recipes within timeframe"""
        cutoff = datetime.now(datetime.UTC) - timedelta(days=timeframe_days)
        
        return self.db.query(Recipe)\
            .filter(Recipe.created_at >= cutoff)\
            .order_by(desc(Recipe.view_count))\
            .limit(limit)\
            .all()

    def delete_recipe(self, recipe_id: str, user_id: str) -> bool:
        """Delete a recipe"""
        recipe = self.get_recipe(recipe_id)
        
        if not recipe or recipe.creator_user_id != user_id:
            return False
            
        self.db.delete(recipe)
        self.db.commit()
        return True