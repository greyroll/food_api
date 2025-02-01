import json
from pathlib import Path
from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select, func

class FoodDB(SQLModel, table=True):
	__tablename__ = "foods"
	id: Optional[int] = Field(default=None, primary_key=True)
	icon: str
	name: str
	cat: str
	kcal: int

	def __str__(self):
		return f"Food(id={self.id}, icon={self.icon}, name={self.name}, cat={self.cat}, kcal={self.kcal})"


class ORMManager:
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

	def add_all(self, objs: list[SQLModel]):
		"""Добавляет список объектов SQLModel в базу данных."""
		with Session(self.engine) as session:
			session.add_all(objs)
			session.commit()
			session.refresh(objs)

	def fetch_all(self) -> list[FoodDB]:
		"""Возвращает список всех записей FoodDB из базы данных."""
		with Session(self.engine) as session:
			statement = select(FoodDB)
			appointments = list(session.exec(statement).fetchall())
		return appointments

	def fetch_all_names(self) -> list[str]:
		"""Возвращает список имен всех записей FoodDB."""
		with Session(self.engine) as session:
			statement = select(FoodDB.name)
			food_names = list(session.exec(statement).fetchall())
		return food_names

	def fetch_by_name(self, name: str) -> FoodDB:
		"""Возвращает записи FoodDB, у которых имя соответствует заданному."""
		with Session(self.engine) as session:
			statement = select(FoodDB).where(FoodDB.name == name)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_by_cat(self, cat: str) -> list[FoodDB]:
		"""Возвращает записи FoodDB из указанной категории."""
		with Session(self.engine) as session:
			statement = select(FoodDB).where(FoodDB.cat == cat)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_by_kcal(self, kcal: int) -> list[FoodDB]:
		"""Возвращает записи FoodDB с калорийностью, равной заданному значению."""
		with Session(self.engine) as session:
			statement = select(FoodDB).where(FoodDB.kcal == kcal)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_food_between_kcal(self, min_kcal: int, max_kcal: int) -> list[FoodDB]:
		"""Возвращает записи FoodDB с калорийностью между min_kcal и max_kcal."""
		with Session(self.engine) as session:
			statement = select(FoodDB).where(FoodDB.kcal >= min_kcal, FoodDB.kcal <= max_kcal)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_max_kcal_food(self) -> FoodDB:
		"""Возвращает запись FoodDB с максимальной калорийностью."""
		with Session(self.engine) as session:
			statement = select(FoodDB).order_by(FoodDB.kcal.desc()).limit(1)
			max_kcal = session.exec(statement).first()
			return max_kcal

	def fetch_min_kcal_food(self) -> FoodDB:
		"""Возвращает запись FoodDB с минимальной калорийностью."""
		with Session(self.engine) as session:
			statement = select(FoodDB).order_by(FoodDB.kcal).limit(1)
			min_kcal = session.exec(statement).first()
			return min_kcal

	@staticmethod
	def convert_from_json_to_food(json_file: str) -> list[FoodDB]:
		"""Преобразует JSON-файл в список объектов FoodDB."""
		with open(json_file, "r", encoding="utf-8") as f:
			data = json.load(f)
			foods = [FoodDB(**item) for item in data]
			return foods