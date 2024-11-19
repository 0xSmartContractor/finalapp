from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime, timedelta
import logging
from uuid import uuid4

from app.database.models import Recipe as DBRecipe, MealPlan as DBMealPlan, MealPlanDay as DBMealPlanDay
from app.schemas.meal_plans import MealPlan as MealPlanSchema
from app.schemas.recipes import Recipe as RecipeSchema
from app.services.recipe_generator import RecipeGeneratorService

logger = logging.getLogger(__name__)

class MealPlanGenerator:
    def __init__(self, db: Session):
        self.db = db
        self.recipe_generator = RecipeGeneratorService(db)

    async def generate_week_plan(self, user_id: str, start_date: datetime) -> MealPlanSchema:
        """Generate a week of meals optimizing for ingredient usage"""
        inventory = {}  # Track available ingredients
        meal_plan = DBMealPlan(
            id=str(uuid4()),
            user_id=user_id, 
            start_date=start_date,
            end_date=start_date + timedelta(days=7),
            is_generated=False,
            generation_status="in_progress"
        )
        
        try:
            for day_num in range(7):
                current_date = start_date + timedelta(days=day_num)
                day_plan = DBMealPlanDay(date=current_date)
                
                # Morning: Check inventory and planned leftover usage
                inventory = self._update_daily_inventory(inventory, day_num)
                
                # Generate meals considering inventory
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    suitable_recipes = self._get_suitable_recipes(
                        meal_type=meal_type,
                        inventory=inventory
                    )
                    
                    # Optimize recipe selection based on inventory
                    optimized_recipes = self._optimize_ingredient_usage(
                        suitable_recipes,
                        inventory,
                        days_ahead=7-day_num
                    )
                    
                    if optimized_recipes:
                        selected_recipe = optimized_recipes[0][0]
                        # Update inventory with new ingredients and leftovers
                        inventory = self._update_inventory_after_meal(
                            inventory,
                            selected_recipe
                        )
                        
                        setattr(day_plan, meal_type, selected_recipe.id)
                
                meal_plan.days.append(day_plan)
            
            meal_plan.is_generated = True
            meal_plan.generation_status = "completed"
            
            self.db.add(meal_plan)
            self.db.commit()
            self.db.refresh(meal_plan)
            
            return MealPlanSchema.from_orm(meal_plan)
            
        except Exception as e:
            logger.error(f"Meal plan generation failed: {str(e)}")
            self.db.rollback()
            raise

    def _get_suitable_recipes(
        self,
        meal_type: str,
        inventory: Dict[str, float]
    ) -> List[DBRecipe]:
        """Get recipes suitable for the meal type and available ingredients"""
        query = self.db.query(DBRecipe).filter(
            DBRecipe.meal_type == meal_type
        )
        
        return query.all()

    def _optimize_ingredient_usage(self, 
        available_recipes: List[DBRecipe], 
        current_inventory: Dict[str, float],
        days_ahead: int
    ) -> List[tuple[DBRecipe, float]]:
        """Find recipes that can use existing ingredients"""
        optimized_recipes = []
        
        for recipe in available_recipes:
            score = self._calculate_ingredient_usage_score(
                recipe,
                current_inventory
            )
            optimized_recipes.append((recipe, score))
        
        return sorted(optimized_recipes, key=lambda x: x[1], reverse=True)

    def _calculate_ingredient_usage_score(self, 
        recipe: DBRecipe, 
        inventory: Dict[str, float]
    ) -> float:
        """Calculate how well a recipe uses existing ingredients"""
        score = 0
        for ingredient in recipe.ingredients:
            if ingredient['item'] in inventory:
                # Higher score for using ingredients that would go bad soon
                days_left = inventory[ingredient['item']].get('days_until_expiry', 0)
                amount_available = inventory[ingredient['item']].get('amount', 0)
                
                if days_left <= 2:
                    score += 3
                elif days_left <= 4:
                    score += 2
                
                if amount_available >= ingredient['amount']:
                    score += 1
                elif amount_available >= (ingredient['amount'] * 0.75):
                    score += 0.5
                    
        return score

    def _update_daily_inventory(self, 
        inventory: Dict[str, float], 
        day_num: int
    ) -> Dict[str, float]:
        """Update inventory for a new day"""
        updated_inventory = inventory.copy()
        
        # Remove expired ingredients
        for ingredient, data in list(updated_inventory.items()):
            data['days_until_expiry'] -= 1
            if data['days_until_expiry'] <= 0:
                del updated_inventory[ingredient]
            
        return updated_inventory

    def _update_inventory_after_meal(self, 
        inventory: Dict[str, float], 
        recipe: DBRecipe
    ) -> Dict[str, float]:
        """Update inventory after a meal is cooked"""
        updated_inventory = inventory.copy()
        
        for ingredient in recipe.ingredients:
            ingredient_name = ingredient['item']
            
            # Remove used amounts
            if ingredient_name in updated_inventory:
                updated_inventory[ingredient_name]['amount'] -= ingredient['amount']
                if updated_inventory[ingredient_name]['amount'] <= 0:
                    del updated_inventory[ingredient_name]
            
            # Add new leftover amounts if specified
            if ingredient.get('yields_leftover'):
                leftover_amount = ingredient['amount'] * ingredient.get('leftover_ratio', 0.5)
                if ingredient_name in updated_inventory:
                    updated_inventory[ingredient_name]['amount'] += leftover_amount
                else:
                    updated_inventory[ingredient_name] = {
                        'amount': leftover_amount,
                        'days_until_expiry': ingredient.get('shelf_life', 3),
                        'from_recipe': recipe.id
                    }
                    
        return updated_inventory