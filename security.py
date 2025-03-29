import os
from functools import wraps

from fastapi import Depends, Cookie, HTTPException, status

from classes.jwt_manager import JWTManager

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
jwt_manager = JWTManager(secret_key=ACCESS_TOKEN_SECRET)


async def authenticate(access_token: str = Cookie(default=None)):
	print(access_token)
	if not access_token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Access token missing"
		)
	# Декодируем токен с помощью твоего менеджера JWT
	payload = jwt_manager.verify_token(access_token)
	if payload is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid or expired token"
		)
	# Обычно в поле "sub" хранится информация об идентификаторе пользователя (например, email)
	user_email = payload.get("sub")
	if not user_email:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token payload"
		)
	return True



