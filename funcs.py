from typing import Optional

from classes.food_manager import FoodManager
from classes.pydantic_model import Food


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
