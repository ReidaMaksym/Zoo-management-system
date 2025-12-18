from src.id_generator import get_next_id
from src.animal import Animal

class Cage:

    def __init__(self) -> None:
        self.id = get_next_id("cage")
        self.animals = []
    

    def __str__(self) -> str:
        return f"Cage with id: {self.id} and animals: {self.animals}"


    def __repr__(self) -> str:
        return f"<Cage, id: {self.id}, animals: {self.animals}>"
    

    def add_animal_to_cage(self, animal: Animal):
        self.animals.append(animal)