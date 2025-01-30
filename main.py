import uvicorn
from fastapi import FastAPI, HTTPException, Query

from orm_model import FoodManager

app = FastAPI()

orm_manager = FoodManager()

@app.get("/hello")
async def hello():
	return {"message": "Hello World"}


# **Задача 1**
# Получите все записи, которые есть в базе и выведите
@app.get("/all_food")
async def get_all_food():
	food_names = orm_manager.fetch_all_names()
	food_names = "\n".join(food_names)

	return {"message": food_names}


# **Задача 2**
# Получите строку в которой `name = Cookie` и выведите
@app.get("/food_name")
async def get_food_by_name(name: str):
	food = orm_manager.fetch_by_name(name.capitalize())

	if not food:
		raise HTTPException(status_code=404, detail="Food not found")

	return {"message": food.icon + " " + food.name + " " + str(food.kcal)}


# Задача 3 и 4
# Получите все продукты из категории
@app.get("/food_cat")
async def get_food_by_cat(cat: str):
	foods = orm_manager.fetch_by_cat(cat)

	if not foods:
		raise HTTPException(status_code=404, detail="Food not found")

	foods_result = ", ".join([food.icon + " " + food.name + " " + str(food.kcal) for food in foods])

	return {"message": foods_result}

# **Задача 5**
# Получите все продукты с калорийностью ниже 200 и выведите в формате
@app.get("/food_max_cal")
async def get_food_max_cal(cal: int = Query(le=200)):
	foods = orm_manager.fetch_food_between_kcal(0, cal)

	if not foods:
		raise HTTPException(status_code=404, detail="Food not found")

	foods_result = ", ".join([food.icon + " " + food.name + " " + str(food.kcal) for food in foods])

	return {"message": foods_result}

# **Задача 6**
# Получите все продукты из категории `veggie` с сортировкой по алфавиту и выведите в формате
@app.get("/food_cat_sort_alph")
async def get_food_by_cat_and_sort_alph(cat: str):
	foods = orm_manager.fetch_by_cat(cat)

	if not foods:
		raise HTTPException(status_code=404, detail="Food not found")

	foods.sort(key=lambda x: x.name)
	foods_result = ", ".join([food.icon + " " + food.name + " " + str(food.kcal) for food in foods])

	return {"message": foods_result}

# **Задача 7**
# Получите все продукты из категории `sweets` c сортировкой по `калорийности` по убыванию и выведите в формате
@app.get("/food_cat_sort_by_kcal")
async def get_food_by_cat_and_sort_by_kcal(cat: str):
	foods = orm_manager.fetch_by_cat(cat)

	if not foods:
		raise HTTPException(status_code=404, detail="Food not found")

	foods.sort(key=lambda x: x.kcal, reverse=True)
	foods_result = ", ".join([food.icon + " " + food.name + " " + str(food.kcal) for food in foods])

	return {"message": foods_result}

# **Задача 9**
# # Выведите самый калорийный продукт и самый некалорийный продукт в формате
@app.get("/food_min_max_kcal")
async def get_food_min_max_kcal():
	min_food = orm_manager.fetch_min_kcal_food()
	max_food = orm_manager.fetch_max_kcal_food()
	return {"message": {"min_food": min_food, "max_food": max_food}}

uvicorn.run(app, host="127.0.0.1", port=8001)