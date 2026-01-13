from src.id_generator import get_next_id

class User:

    def __init__(self, name: str, role: str, responsible_cages = None, shift_is_active = False) -> None:
        self.id = get_next_id("user")
        self.name = name
        self.role = role
        self.responsible_cages = responsible_cages if responsible_cages is not None else []
        self.shift_is_active = shift_is_active
    

    def __str__(self) -> str:
        return f"{self.name}, the user has role: {self.role}"
    

    def __repr__(self) -> str:
        return f"<User; id: {self.id}, name:{self.name}, role: {self.role}, shift_is_active: {self.shift_is_active}>"
    

    def start_shift(self):
        self.shift_is_active = True
    

    def end_shift(self):
        self.shift_is_active = False