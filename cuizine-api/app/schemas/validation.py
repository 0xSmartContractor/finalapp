from pydantic import BaseModel, Field
from typing import Optional

class IngredientValidation(BaseModel):
    name: str
    amount: float = Field(..., gt=0)
    unit: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "chicken breast",
                "amount": 500,
                "unit": "g"
            }
        }

class RecipeValidationError(BaseModel):
    field: str
    message: str
    suggestion: Optional[str] = None