from src.id_generator import get_next_id
from typing import TypedDict, Unpack


class AnimalFields(TypedDict):
    name: str
    age: str
    animal_type: str


class MammalFields(AnimalFields):
    species: str
    breed: str
    fur_color: str


class BirdFields(AnimalFields):
    wing_span: str
    can_fly: str


class ReptileFields(AnimalFields):
    is_venomus: str



class Animal:

    def __init__(self, **kwargs: Unpack[AnimalFields]) -> None:
        self.id = get_next_id("animal")
        self.name = kwargs['name']
        self.age = kwargs['age']
        self.animal_type = kwargs['animal_type']
        # self.id = 0
    

    def __str__(self) -> str:
        return f"Is's {self.animal_type}, his/her name is '{self.name}'"
    

    def __repr__(self) -> str:
        return f"<Animal: animal_type: {self.animal_type}, name: {self.name}, age: {self.age}, id: {self.id}>"


    def make_sound(self) -> str:
        return "Animal makes sound"


class Mammal(Animal):

    def __init__(self, **kwargs: Unpack[MammalFields]) -> None:
        super().__init__(**kwargs)
        self.species = kwargs['species']
        self.breed = kwargs['breed']
        self.fur_color = kwargs['fur_color']
    

class Bird(Animal):

    def __init__(self, **kwargs: Unpack[BirdFields]) -> None:
        super().__init__(**kwargs)
        self.wing_span = kwargs['wing_span']
        self.can_fly = kwargs['can_fly']

    
class Reptile(Animal):

    def __init__(self, **kwargs: Unpack[ReptileFields]) -> None:
        super().__init__(**kwargs)
        self.is_venomus = kwargs['is_venomus']
