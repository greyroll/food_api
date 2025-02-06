from classes.food_orm_model import ORMManager, FoodDB
from classes.pydantic_model import Food


class FoodManager:
	def __init__(self, orm_manager: ORMManager):
		self.orm_manager = orm_manager

	def get_all_food(self) -> list[Food]:
		"""
		Возвращает список всех продуктов.
		"""
		result: list[FoodDB] = self.orm_manager.fetch_all()
		food = list(map(lambda x: Food.model_validate(x), result))
		return food

	def get_by_name(self, name: str) -> list[Food]:
		"""
		Возвращает список продуктов с заданным именем.
		"""
		foods = self.orm_manager.fetch_by_name(name)
		return list(map(lambda x: Food.model_validate(x), foods))

	def get_by_cat(self, cat: str) -> list[Food]:
		"""
		Возвращает список продуктов из заданной категории.
		"""
		foods = self.orm_manager.fetch_by_cat(cat)
		return list(map(lambda x: Food.model_validate(x), foods))

	def get_by_max_kcal(self, kcal: int) -> list[Food]:
		"""
		Возвращает список продуктов с калорийностью не более заданного значения.
		"""
		foods = self.orm_manager.fetch_food_between_kcal(0, kcal)
		return list(map(lambda x: Food.model_validate(x), foods))

	def get_min_max_kcal(self) -> dict:
		"""
		Возвращает продукты с минимальной и максимальной калорийностью.
		"""
		min_food = Food.model_validate(self.orm_manager.fetch_min_kcal_food())
		max_food = Food.model_validate(self.orm_manager.fetch_max_kcal_food())
		return {"min_kcal_food": min_food, "max_kcal_food": max_food}

	def get_min_kcal(self) -> Food:
		"""
		Возвращает продукты с минимальной калорийностью.
		"""
		min_food = Food.model_validate(self.orm_manager.fetch_min_kcal_food())
		return min_food

	def get_max_kcal(self) -> Food:
		"""
		Возвращает продукты с минимальной калорийностью.
		"""
		max_food = Food.model_validate(self.orm_manager.fetch_max_kcal_food())
		return max_food