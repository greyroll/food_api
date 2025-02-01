from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from starlette.middleware.cors import CORSMiddleware

from classes.food_manager import FoodManager
from classes.orm_model import ORMManager

app = FastAPI()

orm_manager = ORMManager()
food_manager = FoodManager(orm_manager)

@app.get("/hello")
async def hello():
	return {"message": "Hello World"}


@app.get("/foods")
async def get_all_food(
    max_kcal: Optional[int] = Query(None, le=200),
    cat: Optional[str] = None,
    name: Optional[str] = None,
	sort_alphabet: Optional[bool] = False,
	sort_kcal: Optional[bool] = False,
	sort_kcal_reverse: Optional[bool] = False,
):
	if max_kcal is not None:
		foods = food_manager.get_by_max_kcal(max_kcal)
	elif cat is not None:
		foods = food_manager.get_by_cat(cat)
	elif name is not None:
		foods = food_manager.get_by_name(name.capitalize())
	else:
		foods = food_manager.get_all_food()

	if sort_alphabet:
		foods.sort(key=lambda x: x.name)
	if sort_kcal:
		foods.sort(key=lambda x: x.kcal)
	if sort_kcal_reverse:
		foods.sort(key=lambda x: x.kcal, reverse=True)

	if not foods:
		raise HTTPException(status_code=404, detail="Food not found")

	return foods


@app.get("/foods/min_max_kcal")
async def get_food_min_max_kcal():
	return food_manager.get_min_max_kcal()

# uvicorn.run(app, host="127.0.0.1", port=8001)

origins = [
    "http://localhost",
    "*"
]

def setup_cors(app):
	app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

setup_cors(app)