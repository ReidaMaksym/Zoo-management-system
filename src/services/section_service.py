from src.domain.section import ZooSection
from src.services.permissions import PermissionService
from src.domain.user import User

class SectionService:

    def __init__(self, permissions: PermissionService) -> None:
        self.permissions = permissions
    

    def add_new_section(self, section_name: str, executor: User):
        """The method creates a new section"""
        
        if not self.permissions.is_authorised(executor, "add"):
            return {"success": False, "message": "Permission denied"}
        
        if len(section_name) == 0:
            return {"success": False, "message": "The section name can't be empty"}
        
        new_section = ZooSection(section_name)

        # self.zoo.sections.append(new_section)

        return {
            "success": True,
            "message": "The section is successfully created",
            "zoo_section": new_section
        }