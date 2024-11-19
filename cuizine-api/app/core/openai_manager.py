from openai import AsyncOpenAI
from app.core.config import settings
from typing import Dict, Any, List
import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class OpenAIManager:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_recipe(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a recipe using OpenAI"""
        try:
            system_prompt = """You are a professional chef and recipe creator. 
            Create detailed, accurate recipes that match the given requirements exactly. 
            The recipe should be creative but practical, with precise measurements and clear instructions.
            Always include preparation time, cooking time, difficulty level, and full nutritional information."""
            
            user_prompt = self._build_recipe_prompt(parameters)
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using latest model for best results
                response_format={"type": "json_object"},
                messages=[  
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7 if parameters.get('recipe_type') == 'crazy' else 0.4,
                max_tokens=4000
            )
            
            recipe_data = json.loads(response.choices[0].message.content)
            return self._validate_recipe_output(recipe_data)
            
        except Exception as e:
            logger.error(f"Recipe generation failed: {str(e)}")
            raise

    def _build_recipe_prompt(self, parameters: Dict[str, Any]) -> str:
        """Build the recipe generation prompt based on parameters"""
        prompt_parts = [
            "Create a detailed recipe with the following requirements:\n",
            f"Recipe Type: {parameters['recipe_type']}\n"
        ]

        if parameters.get('selected_ingredients'):
            prompt_parts.append(f"Must use these ingredients: {', '.join(parameters['selected_ingredients'])}\n")
        
        if parameters.get('meal_type'):
            prompt_parts.append(f"Meal Type: {parameters['meal_type']}\n")
            
        if parameters.get('cuisine'):
            prompt_parts.append(f"Cuisine Style: {parameters['cuisine']}\n")
            
        if parameters.get('dietary_restrictions'):
            prompt_parts.append(f"Dietary Restrictions: {', '.join(parameters['dietary_restrictions'])}\n")
            
        prompt_parts.extend([
            f"Servings: {parameters.get('servings', 2)}\n",
            f"Spicy: {'Yes' if parameters.get('is_spicy') else 'No'}\n",
            "\nPlease provide the recipe in the following JSON format:",
            '''{
                "title": "Recipe Name",
                "description": "Brief description",
                "prep_time": minutes,
                "cook_time": minutes,
                "total_time": minutes,
                "servings": number,
                "difficulty_level": "beginner|intermediate|advanced",
                "ingredients": [
                    {"amount": number, "unit": "string", "item": "string", "notes": "string"}
                ],
                "instructions": [
                    {"step": number, "content": "string", "timing": "string"}
                ],
                "nutritional_info": {
                    "calories": number,
                    "protein": number,
                    "carbs": number,
                    "fat": number
                },
                "equipment_needed": ["string"],
                "tips": ["string"],
                "storage_instructions": "string",
                "leftover_ideas": ["string"]
            }'''
        ])
        
        return "\n".join(prompt_parts)

    def _validate_recipe_output(self, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the generated recipe data"""
        required_fields = {
            'title', 'description', 'prep_time', 'cook_time', 
            'ingredients', 'instructions', 'nutritional_info'
        }
        
        missing_fields = required_fields - set(recipe_data.keys())
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        return recipe_data