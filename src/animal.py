from src.id_generator import get_next_id

class Animal:

    def __init__(self, name: str, age: int, animal_type: str) -> None:
        self.id = get_next_id("animal")
        self.name = name
        self.age = age
        self.animal_type = animal_type
        # self.id = 0
    

    def __str__(self) -> str:
        return f"Is's {self.animal_type}, his/her name is '{self.name}'"
    

    def __repr__(self) -> str:
        return f"<Animal: animal_type: {self.animal_type}, name: {self.name}, age: {self.age}, id: {self.id}>"


    def make_sound(self) -> str:
        return "Animal makes sound"


class Mammal(Animal):

    def __init__(self, name: str, age: int, animal_type: str, species: str, breed: str, fur_color: str) -> None:
        super().__init__(name, age, animal_type)
        # self.id = get_next_id("mammal")
        self.species = species
        self.breed = breed
        self.fur_color = fur_color
    

class Bird(Animal):

    def __init__(self, name: str, age: int, animal_type: str, wing_span: float, can_fly: bool) -> None:
        super().__init__(name, age, animal_type)
        # self.id = get_next_id("bird")
        self.wing_span = wing_span
        self.can_fly = can_fly

    
class Reptile(Animal):

    def __init__(self, name: str, age: int, animal_type: str, is_venomus: bool) -> None:
        super().__init__(name, age, animal_type)
        # self.id = get_next_id("reptile")
        self.is_venomus = is_venomus


