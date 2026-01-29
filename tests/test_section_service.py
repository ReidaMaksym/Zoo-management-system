import pytest
from src.domain.user import User
from src.domain.section import ZooSection
from src.zoo_manager import ZooManager
from src.config.constants import Constants



@pytest.mark.parametrize("section_name,executor,success,message", [
    ("TEST Section 1", User("Test owner", "owner"), True, "The section is successfully created"),
    ("TEST Section 2", User("Test manager", "manager"), True, "The section is successfully created")
])
def test_add_new_section_success(reset_id_generator, zoo_manager, section_name, executor, success, message):
    
    result = zoo_manager.add_new_section(section_name, executor)

    assert result['success'] == success
    assert result['message'] == message
    assert result["zoo_section"].name == section_name

    assert isinstance(result['zoo_section'], ZooSection)
    assert result['zoo_section'] in zoo_manager.zoo.sections


@pytest.mark.parametrize("section_name,executor,success,message", [
    ("Section 1", User("Test wrong role", "test_role"), False, "Permission denied"),
    ("", User("Test owner", "owner"), False, "The section name can't be empty")
])
def test_add_new_section_fail(reset_id_generator, zoo_manager, section_name, executor, success, message):
    
    result = zoo_manager.add_new_section(section_name, executor)

    assert result['success'] == success
    assert result['message'] == message


@pytest.mark.parametrize("section_id,parameters_to_update,success,message", [
    (1, {"name": "New section 1 name"}, True, "The section is successfully updated")
])
def test_edit_section_success(reset_id_generator, zoo_manager, section_id, parameters_to_update, success, message):
    executor = zoo_manager.user_service.users[0]
    result = zoo_manager.edit_section(section_id, parameters_to_update, executor)

    assert result['success'] == success
    assert result['message'] == message

    for key in parameters_to_update:

        assert getattr(result['section'], key) == parameters_to_update[key]


@pytest.mark.parametrize("section_id,parameters_to_update,success,message", [
    (1, {"cages": [1]}, True, "The section is successfully updated"),
    (1, {"cages": [1, 2]}, True, "The section is successfully updated"),
    (1, {"cages": [1, 2, 3]}, True, "The section is successfully updated")
])
def test_edit_section_with_reasign_cage_to_another_section_success(reset_id_generator, zoo_manager, section_id, parameters_to_update, success, message):
    executor = zoo_manager.user_service.users[0]
    result = zoo_manager.edit_section(section_id, parameters_to_update, executor)

    assert result['success'] == success
    assert result['message'] == message

    for cage_id in parameters_to_update['cages']:

        assert result['section'].cages[cage_id - 1].id == cage_id

        assert len(zoo_manager.zoo.sections[1].cages) == 3 - len(parameters_to_update['cages'])


@pytest.mark.parametrize("section_id,executor,parameters_to_update,success,message", [
    (1, User("Test caretaker", "caretaker"), {"name": "Test new name"}, False, "Permission denied"),
    (1, User("Test caretaker", "test"), {"name": "Test new name"}, False, "Permission denied"),
    (100, User("Test owner", "owner"), {"name": "Test new name"}, False, "The section is not found"),
])
def test_edit_section_fail(reset_id_generator, zoo_manager, section_id, parameters_to_update, executor, success, message):
    
    result = zoo_manager.edit_section(section_id, parameters_to_update, executor)

    assert result['success'] == success
    assert result['message'] == message


@pytest.mark.parametrize("section_id,executor,success,message", [
    (1, User("Test Owner", "owner"), True, "The section is successfully deleted"),
    (3, User("Test manager", "manager"), True, "The section is successfully deleted")
])
def test_delete_section_success(reset_id_generator, zoo_manager, section_id, executor, success, message):
    
    result = zoo_manager.delete_section(section_id, executor)


    assert result['success'] == success
    assert result['message'] == message

    for section in zoo_manager.zoo.sections:

        assert section_id != section.id


@pytest.mark.parametrize("section_id,executor,success,message", [
    (1, User("Test caretaker", "caretaker"), False, "Permission denied"),
    (99, User("Test owner", "owner"), False, "The section is not found"),
    (2, User("Test owner", "owner"), False, "The section: 'Section 2' has attached cages. Reassign the cages first")
])
def test_delete_section_fail(reset_id_generator, zoo_manager, section_id, executor, success, message):

    result = zoo_manager.delete_section(section_id, executor)

    assert result['success'] == success
    assert result['message'] == message


def test_get_section_by_id_success(reset_id_generator, zoo_manager):
    
    section_id = 1

    section = zoo_manager.get_section_by_id(section_id)
    assert isinstance(section, ZooSection)
    assert section.id == section_id


def test_get_section_by_id_faild(reset_id_generator, zoo_manager):

    section_id = 99

    result = zoo_manager.get_section_by_id(section_id)
    assert result is None