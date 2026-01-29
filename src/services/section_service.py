from src.domain.section import ZooSection
from src.services.permissions import PermissionService
from src.domain.user import User
from src.domain.zoo import Zoo
from src.config.constants import Constants

class SectionService:

    def __init__(self, zoo: Zoo, permissions: PermissionService) -> None:
        self.permissions = permissions
        self.zoo = zoo
    

    def add_new_section(self, section_name: str, executor: User):
        """The method creates a new section"""
        
        if not self.permissions.is_authorised(executor, "add"):
            return {"success": False, "message": "Permission denied"}
        
        if len(section_name) == 0:
            return {"success": False, "message": "The section name can't be empty"}
        
        new_section = ZooSection(section_name)

        self.zoo.sections.append(new_section)

        return {
            "success": True,
            "message": "The section is successfully created",
            "zoo_section": new_section
        }
    
    
    def get_section_by_id(self, section_id: int) -> ZooSection | None:
        """The method searches for a section and returns it if it is found, otherwise returns None"""

        for section in self.zoo.sections:
            if section.id == section_id:
                return section
        
        return None
    

