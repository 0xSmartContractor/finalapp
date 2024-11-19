import pytest
from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy.orm import Session
from app.services.recipe_generator import RecipeGeneratorService
from app.services.shopping_list import ShoppingListService
from app.models.recipes import RecipeGeneratorRequest 
from app.database.models import Recipe as DBRecipe, ShoppingList
from datetime import datetime

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def mock_openai():
    with patch('app.services.recipe_generator.OpenAIManager') as mock:
        mock.return_value.generate_recipe = AsyncMock()
        yield mock

class TestRecipeGeneratorService:
    @pytest.fixture
    def service(self, mock_db, mock_openai):
        return RecipeGeneratorService(mock_db)

    @pytest.mark.asyncio
    async def test_generate_recipe_success(self, service, mock_db, mock_openai):
        # Arrange
        request = RecipeGeneratorRequest(
            recipe_type="custom",
            selected_ingredients=["chicken", "rice"],
            meal_type="dinner",
            servings=4
        )
        mock_recipe_data = {
            "title": "Test Recipe",
            "description": "A test recipe",
            "prep_time": 20,
            "cook_time": 30,
            "ingredients": [
                {"amount": 500, "unit": "g", "item": "chicken"}
            ],
            "instructions": [
                {"step": 1, "content": "Cook chicken"}
            ],
            "nutritional_info": {
                "calories": 400,
                "protein": 30,
                "carbs": 40,
                "fat": 10
            }
        }
        mock_openai.return_value.generate_recipe.return_value = mock_recipe_data

        # Act
        result = await service.generate_recipe(request, "user_123")

        # Assert
        assert result.title == "Test Recipe"
        assert mock_db.add.called
        assert mock_db.commit.called

    @pytest.mark.asyncio
    async def test_generate_recipe_with_preferences(self, service, mock_db):
        # Arrange
        mock_db.query().filter().first.return_value = Mock(
            dietary_restrictions=["vegetarian"],
            cooking_skill_level="intermediate"
        )

        request = RecipeGeneratorRequest(
            recipe_type="custom",
            meal_type="dinner"
        )

        # Act
        await service.generate_recipe(request, "user_123")

        # Assert
        call_args = mock_openai.return_value.generate_recipe.call_args[0][0]
        assert "vegetarian" in call_args["additional_restrictions"]
        assert call_args["skill_level"] == "intermediate"

class TestShoppingListService:
    @pytest.fixture
    def service(self, mock_db):
        return ShoppingListService(mock_db)

    @pytest.mark.asyncio
    async def test_create_list_from_recipe(self, service, mock_db):
        # Arrange
        mock_recipe = Mock(spec=DBRecipe)
        mock_recipe.id = "recipe_123"
        mock_recipe.title = "Test Recipe"
        mock_recipe.servings = 4
        mock_recipe.ingredients = [
            {"amount": 500, "unit": "g", "item": "chicken"},
            {"amount": 200, "unit": "g", "item": "rice"}
        ]
        mock_db.query().filter().first.return_value = mock_recipe

        # Act
        result = await service.create_list_from_recipe(
            "recipe_123",
            "user_123",
            servings=2
        )

        # Assert
        assert result.recipe_id == "recipe_123"
        assert len(result.items) == 2
        assert result.items[0]["amount"] == 250  # Scaled down for 2 servings

    @pytest.mark.asyncio
    async def test_merge_lists(self, service, mock_db):
        # Arrange
        mock_lists = [
            Mock(spec=ShoppingList, items=[
                {"name": "chicken", "amount": 500, "unit": "g"},
            ]),
            Mock(spec=ShoppingList, items=[
                {"name": "chicken", "amount": 500, "unit": "g"},
            ])
        ]
        mock_db.query().filter().all.return_value = mock_lists

        # Act
        result = await service.merge_lists(
            ["list1", "list2"],
            "user_123",
            "Merged List"
        )

        # Assert
        assert result.name == "Merged List"
        assert result.items[0]["amount"] == 1000  # Merged amounts
        assert mock_db.add.called
        assert mock_db.commit.called

    def test_determine_category(self, service):
        # Test category determination
        assert service._determine_category("chicken breast") == "meat"
        assert service._determine_category("tomatoes") == "produce"
        assert service._determine_category("milk") == "dairy"
        assert service._determine_category("soy sauce") == "pantry"
        assert service._determine_category("unknown item") == "other"

@pytest.mark.asyncio
async def test_rate_limiting(mock_db):
    # Test rate limiting functionality
    with patch('app.core.rate_limit.check_rate_limit') as mock_check:
        mock_check.return_value = (False, 0)
        
        request = RecipeGeneratorRequest(recipe_type="custom")
        service = RecipeGeneratorService(mock_db)
        
        with pytest.raises(Exception) as exc:
            await service.generate_recipe(request, "user_123")
        
        assert "rate limit" in str(exc.value).lower()

@pytest.mark.asyncio
async def test_error_handling(mock_db):
    # Test error handling
    with patch('app.core.openai_manager.OpenAIManager.generate_recipe') as mock_generate:
        mock_generate.side_effect = Exception("API Error")
        
        service = RecipeGeneratorService(mock_db)
        request = RecipeGeneratorRequest(recipe_type="custom")
        
        with pytest.raises(Exception) as exc:
            await service.generate_recipe(request, "user_123")
        
        assert "API Error" in str(exc.value)
        assert not mock_db.commit.called