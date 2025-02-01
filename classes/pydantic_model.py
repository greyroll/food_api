from pydantic import BaseModel

class Food(BaseModel):
	icon: str
	name: str
	cat: str
	kcal: int

	class Config:
		from_attributes = True