from src.id_generator import get_next_id
from src.domain.cage import Cage


class ZooSection:

    def __init__(self, name: str, cages = None) -> None:
        self.id = get_next_id("zoo_section")
        self.name = name
        self.cages = cages if cages is not None else []

    
    def __str__(self) -> str:
        return f"{self.name} section, with {len(self.cages)} cages"
    

    def __repr__(self) -> str:
        return f"<Section; id: {self.id}, name: {self.name}, cages: {self.cages}>"
    

    def get_all_cages(self) -> list[Cage]:
        return self.cages
    

    def get_cage_by_id(self, cage_id) -> Cage | None:

        for cage in self.cages:
            if cage.id == cage_id:
                return cage
        
        return None
