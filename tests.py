from classes.food_manager import FoodManager
from classes.orm_model import ORMManager

orm_manager = ORMManager()
food_manager = FoodManager(orm_manager)


def test_create_tables():
	orm_manager.create_all_tables()

def test_convert_from_json_to_food():
	print(orm_manager.convert_from_json_to_food("all_food.json"))

def test_add_all():
	orm_manager.add_all(orm_manager.convert_from_json_to_food("all_food.json"))

def test_all_names():
	print(orm_manager.fetch_all_names())

def test_fetch_by_cat():
	print(orm_manager.fetch_by_cat("veggie"))

def test_fetch_between():
	print(orm_manager.fetch_food_between_kcal(20, 100))

def test_fetch_max_kcal():
	print(orm_manager.fetch_max_kcal_food())

def test_get_all_food():
	print(food_manager.get_all_food())