from typing import Optional
from pathlib import Path

from sqlmodel import Field, SQLModel, Session, create_engine, select, func

class UserDB(SQLModel, table=True):
	__tablename__ = "login"

	id: Optional[int] = Field(default=None, primary_key=True)
	email: str
	password: str


class UserORMManager:
	def __init__(self):
		project_root = Path(__file__).resolve().parent.parent
		db_path = project_root / "food.db"  # Путь к базе данных в корне проекта

		self.engine = create_engine(f"sqlite:///{db_path}")

	def create_all_tables(self):
		SQLModel.metadata.create_all(self.engine)

	def add(self, obj: SQLModel):
		"""Добавляет один объект SQLModel в базу данных."""
		with Session(self.engine) as session:
			session.add(obj)
			session.commit()
			session.refresh(obj)
		return obj

	def add_all(self, objs: list[SQLModel]):
		"""Добавляет список объектов SQLModel в базу данных."""
		with Session(self.engine) as session:
			session.add_all(objs)
			session.commit()
			session.refresh(objs)
		return objs

	def validate_login(self, email: str, password: str) -> Optional[UserDB]:
		with Session(self.engine) as session:
			# Ищем пользователя по email и password
			statement = select(UserDB).where(UserDB.email == email, UserDB.password == password)
			return session.exec(statement).first()

	def get_user_by_email(self, email: str):
		with Session(self.engine) as session:
			# Ищем пользователя по email
			statement = select(UserDB).where(UserDB.email == email)
			return session.exec(statement).first()


