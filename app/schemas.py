from pydantic import BaseModel, HttpUrl, Field

from typing import Sequence
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Recipe(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    label: str = Field(...)
    source: str = Field(...)
    url: HttpUrl = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "label": "Chicken Korma",
                "source": "David's secret recipes",
                "url": "http://www.somenicerecipes.com/recipes/chicken_korma.html",
            }
        }


class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]

