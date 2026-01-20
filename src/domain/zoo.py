
class Zoo:

    def __init__(self, name: str) -> None:
        self.name = name
        self.sections = []

    
    def __str__(self) -> str:
        return f"{self.name} zoo"