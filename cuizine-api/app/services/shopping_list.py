from sqlalchemy.orm import Session
from app.database.models import ShoppingList, Recipe
from app.models.recipes import RecipeIngredient
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

class ShoppingListService:
    def __init__(self, db: Session):
        self.db = db

    async def create_list_from_recipe(
        self,
        recipe_id: str,
        user_id: str,
        servings: Optional[int] = None
    ) -> ShoppingList:
        """Create a shopping list from a recipe"""
        try:
            recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
            if not recipe:
                raise ValueError("Recipe not found")

            # Calculate scaling factor if servings specified
            scale = 1.0
            if servings:
                scale = servings / recipe.servings

            # Process ingredients with scaling
            shopping_items = self._process_recipe_ingredients(recipe.ingredients, scale)

            # Create shopping list
            shopping_list = ShoppingList(
                id=str(uuid4()),
                user_id=user_id,
                recipe_id=recipe_id,
                name=f"Ingredients for {recipe.title}",
                items=shopping_items,
                created_at=datetime.utcnow()
            )

            self.db.add(shopping_list)
            self.db.commit()
            self.db.refresh(shopping_list)

            return shopping_list

        except Exception as e:
            logger.error(f"Error creating shopping list: {str(e)}")
            self.db.rollback()
            raise

    async def merge_lists(
        self,
        list_ids: List[str],
        user_id: str,
        new_list_name: str
    ) -> ShoppingList:
        """Merge multiple shopping lists into one"""
        try:
            # Get all lists and verify ownership
            lists = self.db.query(ShoppingList).filter(
                ShoppingList.id.in_(list_ids),
                ShoppingList.user_id == user_id
            ).all()

            if len(lists) != len(list_ids):
                raise ValueError("One or more lists not found or unauthorized")

            # Merge items
            merged_items = {}
            for shopping_list in lists:
                for item in shopping_list.items:
                    key = f"{item['name']}_{item['unit']}"
                    if key in merged_items:
                        merged_items[key]['amount'] += item['amount']
                    else:
                        merged_items[key] = item.copy()

            # Create new list
            merged_list = ShoppingList(
                id=str(uuid4()),
                user_id=user_id,
                name=new_list_name,
                items=list(merged_items.values()),
                created_at=datetime.utcnow()
            )

            self.db.add(merged_list)
            self.db.commit()
            self.db.refresh(merged_list)

            return merged_list

        except Exception as e:
            logger.error(f"Error merging shopping lists: {str(e)}")
            self.db.rollback()
            raise

    def _process_recipe_ingredients(
        self,
        ingredients: List[Dict[str, Any]],
        scale: float = 1.0
    ) -> List[Dict[str, Any]]:
        """Process and categorize recipe ingredients"""
        shopping_items = []

        for ing in ingredients:
            amount = ing.get('amount', 0) * scale if ing.get('amount') else None
            
            item = {
                "name": ing['item'],
                "amount": round(amount, 2) if amount else None,
                "unit": ing.get('unit'),
                "category": self._determine_category(ing['item']),
                "checked": False,
                "notes": ing.get('notes')
            }
            shopping_items.append(item)

        return sorted(shopping_items, key=lambda x: (x['category'], x['name']))

    def _determine_category(self, ingredient: str) -> str:
        """Determine ingredient category based on name"""
        # This could be enhanced with ML categorization
        categories = {
            'produce': ['lettuce', 'tomato', 'onion', 'garlic', 'vegetable', 'fruit'],
            'meat': ['chicken', 'beef', 'pork', 'fish', 'seafood'],
            'dairy': ['milk', 'cheese', 'yogurt', 'cream', 'butter'],
            'pantry': ['flour', 'sugar', 'oil', 'vinegar', 'spice', 'herb'],
            'frozen': ['frozen']
        }

        ingredient_lower = ingredient.lower()
        for category, keywords in categories.items():
            if any(keyword in ingredient_lower for keyword in keywords):
                return category

        return 'other'

    async def get_user_lists(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[ShoppingList]:
        """Get all shopping lists for a user"""
        return self.db.query(ShoppingList)\
            .filter(ShoppingList.user_id == user_id)\
            .order_by(ShoppingList.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    async def update_list_items(
        self,
        list_id: str,
        user_id: str,
        updates: List[Dict[str, Any]]
    ) -> ShoppingList:
        """Update shopping list items"""
        shopping_list = self.db.query(ShoppingList).filter(
            ShoppingList.id == list_id,
            ShoppingList.user_id == user_id
        ).first()

        if not shopping_list:
            raise ValueError("Shopping list not found or unauthorized")

        # Update items
        items_dict = {f"{item['name']}_{item['unit']}": item 
                     for item in shopping_list.items}
        
        for update in updates:
            key = f"{update['name']}_{update['unit']}"
            if key in items_dict:
                items_dict[key].update(update)

        shopping_list.items = list(items_dict.values())
        shopping_list.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(shopping_list)

        return shopping_list

    async def delete_list(self, list_id: str, user_id: str) -> bool:
        """Delete a shopping list"""
        result = self.db.query(ShoppingList).filter(
            ShoppingList.id == list_id,
            ShoppingList.user_id == user_id
        ).delete()

        self.db.commit()
        return result > 0