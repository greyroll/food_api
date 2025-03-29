import hashlib
from typing import Optional

from classes.food_manager import FoodManager
from classes.jwt_manager import JWTManager
from classes.pydantic_model import Food
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.requests import Request


def process_food_query(
    max_kcal: Optional[int],
    cat: Optional[str],
    name: Optional[str],
    sort_alphabet: bool,
    sort_kcal: bool,
    sort_kcal_reverse: bool,
	food_manager: FoodManager) -> list[Food] | None:

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

    return foods

#
# def verify_user(jwt_manager: JWTManager, access_token: str = Cookie(default=None)):
#     if not access_token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Access token missing"
#         )
#         # Декодируем токен с помощью твоего менеджера JWT
#     payload = jwt_manager.verify_token(access_token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )
#     # Обычно в поле "sub" хранится информация об идентификаторе пользователя (например, email)
#     user_email = payload.get("sub")
#     if not user_email:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token payload"
#         )
