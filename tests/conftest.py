import pytest
from src.domain.user import User
from src.zoo_manager import ZooManager
from src.domain.zoo import Zoo
from src.id_generator import current_id
from src.services.user_service import UserService
from src.services.permissions import PermissionService
from src.services.section_service import SectionService


@pytest.fixture(autouse=True)
def reset_id_generator():
    current_id.clear()


@pytest.fixture
def zoo_manager():

    zoo = Zoo("Test name")
    users = [User("Owner", "owner"), User("Manager", "manger"), User("Caretaker", "caretaker")]
    permissions = PermissionService()
    user_service = UserService(permissions)
    secrion_service = SectionService(permissions)
    zoo_manager = ZooManager(zoo, user_service, permissions, secrion_service)

    for user in users:
        user_service.users.append(user)
        
    return zoo_manager

@pytest.fixture
def owner_user():
    return User("Owner", "owner")

@pytest.fixture
def manager_user():
    return User("Manager", "manager")

@pytest.fixture()
def caretaker_user():
    return User("Caretaker", "caretaker")