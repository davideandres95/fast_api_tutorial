import os
from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse

from typing import Optional, Any
from pathlib import Path

from app.schemas import RecipeSearchResults, Recipe
from app.recipe_data import RECIPES

from bson import ObjectId
import motor.motor_asyncio

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.RECIPES

api_router = APIRouter()

@api_router.get("/", status_code=200)
async def root(request: Request) -> dict:
    """
    Root Get
    """
    recipes = await db["RECIPES"].find().to_list(10)
    return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "recipes": recipes},
    )

@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
async def fetch_recipe(*, recipe_id: str) -> dict:
    """
    Fetch a single recipe by ID
    """
    if (recipe := await db["RECIPES"].find_one({"_id": recipe_id})) is not None:
        return recipe

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")


@api_router.get("/search/", status_code=200)
async def search_recipes(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="Chicken"),
        max_results: Optional[int] = 10
   ) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python List slicing to limit results
        # based on the max_results query parameter
        results = await db["RECIPES"].find().to_list(max_results)
        return {"results": results}

    results = await db["RECIPES"].find({"label": {"$regex": '{}'.format(keyword),
                                                  "$options": 'i' # case insensitive
                                                 }
                                }).to_list(100)
    print(results)
    return {"results": list(results)[:max_results]}

@api_router.post("/recipe/", status_code=201, response_model=Recipe)
async def create_recipe(*, recipe_in: Recipe) -> dict:
    """
    Create a new recipe (in memory only)
    """

    recipe = jsonable_encoder(recipe_in)
    new_recipe = await db["RECIPES"].insert_one(recipe)
    created_recipe = await db["RECIPES"].find_one({"_id": new_recipe.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recipe)


@api_router.delete("/recipe/{recipe_id}", response_description="Delete a Recipe")
async def delete_recipe(*, recipe_id: str):
    delete_result = await db["RECIPES"].delete_one({"_id": recipe_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Recipe {} not found".format(recipe_id))

app.include_router(api_router)

