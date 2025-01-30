import json
from pathlib import Path
from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select, func

class Food(SQLModel, table=True):
	__tablename__ = "foods"
	id: Optional[int] = Field(default=None, primary_key=True)
	icon: str
	name: str
	cat: str
	kcal: int

	def __str__(self):
		return f"Food(id={self.id}, icon={self.icon}, name={self.name}, cat={self.cat}, kcal={self.kcal})"


class FoodManager:
	def __init__(self):
		project_root = Path(__file__).resolve().parent
		db_path = project_root / "food.db"  # Путь к базе данных в корне проекта

		self.engine = create_engine(f"sqlite:///{db_path}")

	def create_all_tables(self):
		SQLModel.metadata.create_all(self.engine)

	def add(self, obj: SQLModel):
		with Session(self.engine) as session:
			session.add(obj)
			session.commit()
			session.refresh(obj)

	def add_all(self, objs: list[SQLModel]):
		with Session(self.engine) as session:
			session.add_all(objs)
			session.commit()
			session.refresh(objs)

	def fetch_all(self) -> list[Food]:
		with Session(self.engine) as session:
			statement = select(Food)
			appointments = list(session.exec(statement).fetchall())
		return appointments

	def fetch_all_names(self) -> list[str]:
		with Session(self.engine) as session:
			statement = select(Food.name)
			food_names = list(session.exec(statement).fetchall())
		return food_names

	def fetch_by_name(self, name: str) -> Food:
		with Session(self.engine) as session:
			statement = select(Food).where(Food.name == name)
			food = session.exec(statement).first()
		return food

	def fetch_by_cat(self, cat: str) -> list[Food]:
		with Session(self.engine) as session:
			statement = select(Food).where(Food.cat == cat)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_by_kcal(self, kcal: int) -> list[Food]:
		with Session(self.engine) as session:
			statement = select(Food).where(Food.kcal == kcal)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_food_between_kcal(self, min_kcal: int, max_kcal: int) -> list[Food]:
		with Session(self.engine) as session:
			statement = select(Food).where(Food.kcal >= min_kcal, Food.kcal <= max_kcal)
			foods = session.exec(statement).fetchall()
		return foods

	def fetch_max_kcal_food(self) -> Food:
		with Session(self.engine) as session:
			statement = select(Food).order_by(Food.kcal.desc()).limit(1)
			max_kcal = session.exec(statement).first()
			return max_kcal

	def fetch_min_kcal_food(self) -> Food:
		with Session(self.engine) as session:
			statement = select(Food).order_by(Food.kcal).limit(1)
			min_kcal = session.exec(statement).first()
			return min_kcal

	@staticmethod
	def convert_from_json_to_food(json_file: str) -> list[Food]:
		with open(json_file, "r", encoding="utf-8") as f:
			data = json.load(f)
			foods = [Food(**item) for item in data]
			return foods