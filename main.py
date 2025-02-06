import os
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request, Header, Cookie, Form
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from classes.food_manager import FoodManager
from classes.food_orm_model import ORMManager
from classes.user_orm_model import UserORMManager
from funcs import process_food_query

app = FastAPI()
templates = Jinja2Templates(directory="templates")

load_dotenv()

# Получаем секретное значение токена из переменной окружения
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

orm_manager = ORMManager()
food_manager = FoodManager(orm_manager)
user_manager = UserORMManager()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user_agent: str = Header(), access_token: Optional[str] = Cookie(default=None)):
	if "Chrome" in user_agent:
		pass
	elif "Safari" in user_agent:
		raise HTTPException(detail="We don't eat apples", status_code=403)

	if access_token is None or access_token != "food123":
		return RedirectResponse(url="/login", status_code=302)

	template_response = templates.TemplateResponse(request=request, name="index.html")


	return template_response


@app.get("/foods", response_class=HTMLResponse)
async def get_all_food(
	request: Request,
    max_kcal: Optional[int] = Query(None, le=200),
    cat: Optional[str] = None,
    name: Optional[str] = None,
	sort_alphabet: Optional[bool] = False,
	sort_kcal: Optional[bool] = False,
	sort_kcal_reverse: Optional[bool] = False,
	access_token: Optional[str] = Cookie(default=None),
):
	if access_token is None or access_token != "food123":
		raise HTTPException(status_code=401, detail="Unauthorized")

	foods = process_food_query(max_kcal, cat, name, sort_alphabet, sort_kcal, sort_kcal_reverse, food_manager)

	if not foods:
		raise HTTPException(status_code=404, detail="Food not found")

	foods_data = [food.model_dump() for food in foods]

	template_response = templates.TemplateResponse(request=request, name="foods.html", context={"foods": foods_data})
	template_response.set_cookie(key="access_token", value="food123")

	return template_response


@app.get("/foods/min_max_kcal", response_class=HTMLResponse)
async def get_food_min_max_kcal(request: Request, access_token: Optional[str] = Cookie(default=None)):
	if access_token is None or access_token != "food123":
		raise HTTPException(status_code=401, detail="Unauthorized")

	min_food = food_manager.get_min_kcal().model_dump()
	max_food = food_manager.get_max_kcal().model_dump()
	template_response = templates.TemplateResponse(request=request, name="min_max_kcal.html", context={"min_food": min_food, "max_food": max_food})

	return template_response

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):

	templates_response = templates.TemplateResponse(request=request, name="login.html")

	return templates_response

@app.post("/validate_login", response_class=HTMLResponse)
async def login_form(request: Request, email: str = Form(...), password: str = Form(...)):

	if user_manager.validate_login(email, password) is None:
		raise HTTPException(status_code=401, detail="Invalid email or password")

	templates_response = templates.TemplateResponse(request=request, name="validate_login.html")
	templates_response.set_cookie(
		key="access_token",
        value=ACCESS_TOKEN_SECRET,
        httponly=True,  # Ограничиваем доступ из JS
        secure=True,    # Для HTTPS соединений
        samesite="lax"
	)

	return templates_response


@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
	templates_response = templates.TemplateResponse(request=request, name="logout.html")
	templates_response.delete_cookie(key="access_token")
	return templates_response


uvicorn.run(app, host="127.0.0.1", port=8001)

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