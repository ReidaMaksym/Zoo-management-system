import pytest
from src.domain.user import User
from src.domain.section import ZooSection
from src.zoo_manager import ZooManager
from src.config.constants import Constants



@pytest.mark.parametrize("section_name,executor,success,message", [
    ("Section 1", User("Test owner", "owner"), True, "The section is successfully created"),
    ("Section 2", User("Test manager", "manager"), True, "The section is successfully created")
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

