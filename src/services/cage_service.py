from src.services.permissions import PermissionService
from src.config.constants import Constants

class CageService:

    def __init__(self, permissions: PermissionService) -> None:
        self.permissions = permissions