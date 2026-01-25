import pytest
from src.domain.user import User
from src.zoo_manager import ZooManager
from src.domain.zoo import Zoo
from src.id_generator import current_id

@pytest.fixture(autouse=True)
def reset_id_generator():
    current_id.clear()


@pytest.fixture
def zoo_manager():

    zoo = Zoo("Test name")
    users = [User("Owner", "owner"), User("Manager", "manger"), User("Caretaker", "caretaker")]
    zoo_manager = ZooManager(zoo)

    for user in users:
        zoo_manager.users.append(user)
        
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
    

@pytest.mark.parametrize("executor,target_user,expected", [
    (User(name="Test owner", role="owner"), User(name="Test manager", role="manager"), True),
    
    (User(name="Test owner", role="owner"), User(name="Test caretaker", role="caretaker"), True),

    (User(name="Test manager", role="manager"), User(name="Test caretaker", role="caretaker"), True),

    (User(name="Test manager 1", role="manager"), User(name="Test manager 2", role="manager"), False),

    (User(name="Test manager", role="manager"), User(name="Test owner", role="owner"), False),

    (User(name="Test caretaker", role="caretaker"), User(name="Test manager 1", role="manager"), False),

    (User(name="Test caretaker 1", role="caretaker"), User(name="Test caretaker 2", role="caretaker"), False),
])
def test_can_edit_user(zoo_manager, executor, target_user, expected):

    result = zoo_manager.can_edit_user(executor, target_user)

    assert result == expected


def test_can_user_edit_themself(zoo_manager, owner_user, manager_user, caretaker_user):

    assert zoo_manager.can_edit_user(owner_user, owner_user) == True
    assert zoo_manager.can_edit_user(manager_user, manager_user) == True
    assert zoo_manager.can_edit_user(caretaker_user, caretaker_user) == True


@pytest.mark.parametrize("name,role,executor,success,message", [
    ("Test 1", "manager", User("Owner", "owner"), True, "The user is successfully created"),
    ("Test 2", "caretaker", User("Owner", "owner"), True, "The user is successfully created"),
    ("Test 3", "manager", User("Manager", "manager"), True, "The user is successfully created"),
    ("Test 4", "caretaker", User("Manager", "manager"), True, "The user is successfully created")
])
def test_add_new_user_success(zoo_manager, name, role, executor, success, message):
    
    new_user = zoo_manager.add_new_user(name, role, executor)

    assert new_user['success'] == success
    assert new_user['message'] == message

    assert isinstance(new_user['user'], User)

    assert new_user['user'].name == name
    assert new_user['user'].role == role

    assert new_user['user'] in zoo_manager.users


@pytest.mark.parametrize("name,role,executor,success,message", [
    ("Test 1", "owner", User("Owner", "owner"), False, "Provided role does not exist"),
    ("Test 2", "manager", User("Caretaker", "caretaker"), False, "Permission denied")
])
def test_add_new_user_fail(zoo_manager, name, role, executor, success, message):
    
    new_user = zoo_manager.add_new_user(name, role, executor)

    assert new_user['success'] == success
    assert new_user['message'] == message


@pytest.mark.parametrize("user_id,parameters_to_update,success,message", [
    (2, {"role": "caretaker"}, True, "The user is successfully updated"),
    (2, {"name": "New name"}, True, "The user is successfully updated"),
    (2, {"responsible_cages": [1, 2, 3]}, True, "The user is successfully updated"),
    (2, {"name": "New name", "role": "caretaker", "responsible_cages": [1, 2, 3]}, True, "The user is successfully updated"),
    (2, {"id": 99}, True, "The user is successfully updated")
])
def test_edit_user_success(reset_id_generator ,zoo_manager, user_id, parameters_to_update, success, message):
    executor = zoo_manager.users[0]
    result = zoo_manager.edit_user(user_id, executor, parameters_to_update)

    assert result['success'] == success
    assert result['message'] == message

    for key in parameters_to_update:
        if key == "id":
            continue
        assert getattr(result['user'], key) == parameters_to_update[key]
    

@pytest.mark.parametrize("user_id,executor,parameters_to_update,success,message", [
    (2, User("Test", "test"), {"name": "New name"}, False, "Permission denied"),
    (999, User("Owner", "owner"), {"name": "New name"},False, "The user is not found")
])
def test_edit_user_fail(reset_id_generator, zoo_manager, user_id, executor,parameters_to_update ,success, message):
    
    result = zoo_manager.edit_user(user_id, executor, parameters_to_update)

    assert result['success'] == success
    assert result['message'] == message


@pytest.mark.parametrize("user_id,success,message", [
    (2, True, "The user is successfully deleted"),
    (3, True, "The user is successfully deleted")
])
def test_delete_user_success(reset_id_generator, zoo_manager, user_id, success, message):
    executor = zoo_manager.users[0]
    result = zoo_manager.delete_user(user_id, executor)

    assert result['success'] == success
    assert result['message'] == message


@pytest.mark.parametrize("user_id,executor,success,message", [
    (2, User("Test manager", "manager"), False, "Permission denied"),
    (2, User("Test caretaker", "caretaker"), False, "Permission denied"),
    (999, User("Test owner", "owner"), False, "The user is not found")
])
def test_delete_user_fail(reset_id_generator, zoo_manager, user_id, executor, success, message):
    result = zoo_manager.delete_user(user_id, executor)

    assert result['success'] == success
    assert result['message'] == message


def test_get_user_by_id_susscess(reset_id_generator, zoo_manager):
    
    user_id = 2

    result = zoo_manager.get_user_by_id(user_id)

    assert isinstance(result, User)
    assert result.id == user_id


def test_get_user_by_id_fail(reset_id_generator, zoo_manager):

    user_id = 99

    result = zoo_manager.get_user_by_id(user_id)

    assert result is None