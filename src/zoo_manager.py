from src.animal import Animal, Mammal, Bird, Reptile
from src.cage import Cage
from src.section import ZooSection
from src.user import User
from src.zoo import Zoo

AUTHORISED_ROLES = {
    'add': ['owner', 'manager'],
    'edit': ['owner', 'manager', 'caretaker'],
    'delete': ['owner'],
    'edit_section': ['owner', 'manager'],
    'delete_section': ['owner', 'manager'],
    'delete_cage': ['owner', 'manager'],
    'add_animal': ['owner', 'manager', 'caretaker'],
    'delete_animal': ['owner', 'manager', 'caretaker']
}


AVAILABLE_ROLES = ['manager', 'caretaker']


EDITABLE_FIELDS = {
    "user": ['name', 'role', 'responsible_cages', 'shift_is_active'],
    "section": ["name", "cages"],
    "cage": ['animals'],
    "animal": ['name', 'age', 'fur_color', 'wing_span', 'can_fly']
}


class ZooManager:

    def __init__(self, zoo: Zoo) -> None:
        self.zoo = zoo
        self.users = []

    
    def is_authorised(self, executor: User, operation: str) -> bool:
        """The method determines whether the user is allowed to make an operation or not"""
        if operation == 'add':
            return executor.role in AUTHORISED_ROLES["add"]
        
        elif operation == 'edit':
            return executor.role in AUTHORISED_ROLES["edit"]
        
        elif operation == 'delete':
            return executor.role in AUTHORISED_ROLES["delete"]
        
        elif operation == 'edit_section':
            return executor.role in AUTHORISED_ROLES["edit_section"]
        
        elif operation == 'delete_section':
            return executor.role in AUTHORISED_ROLES["delete_section"]
        
        elif operation == 'delete_cage':
            return executor.role in AUTHORISED_ROLES['delete_cage']
        
        elif operation == 'add_animal':
            return executor.role in AUTHORISED_ROLES["add_animal"]
        
        elif operation == 'delete_animal':
            return executor.role in AUTHORISED_ROLES['delete_animal']
        
        else:
            return False


    # ------ User logic ------
    def can_edit_user(self, executor: User, target_user: User) -> bool:
        """The method determines whether the executor can edit another user based on the executor's role"""

        if executor.role == 'owner':
            return True
        
        if executor.role == 'manager':
            if target_user.role == 'caretaker':
                return True
            if executor.id == target_user.id:
                return True
        
        if executor.role == 'caretaker':
            return executor.id == target_user.id
        
        return False
    

    def add_new_user(self, name: str, role: str, executor: User) -> dict:
        """The method creates a new user"""

        if not self.is_authorised(executor, 'add'):
            return {"success": False, "message": "Permission denied"}

        new_user = User(name, role)
        self.users.append(new_user)

        return {
            "success": True,
            "message": "The user is successfully created",
            "user": new_user
        }


    def edit_user(self, user_id: int, executor: User, parameters_to_update: dict):
        """The method finds the user by its ID and edits it by the specified parameters"""
        
        if not self.is_authorised(executor, "edit"):
            return {"success": False, "message": "Permission denied"}

        editable_user = self.get_user_by_id(user_id)

        if not editable_user:
            return {"success": False, "message": "The user is not found"}
        
        if not self.can_edit_user(executor, editable_user):
            return {"success": False, "message": "Permission denied"}
        
        for key, value in parameters_to_update.items():
            if key == 'id':
                continue

            if key in EDITABLE_FIELDS["user"]:
                setattr(editable_user, key, value)
        
        return {
            "success": True,
            "message": "The user is successfully updated",
            "user": editable_user
        }


    def delete_user(self, user_id: int, executor: User) -> dict:
        """The method deletes the user if the user is found"""
        
        if not self.is_authorised(executor, "delete"):
            return {"success": False, "message": "Permission denied"}
        
        target_user = self.get_user_by_id(user_id)

        if not target_user:
            return {"success": False, "message": "The user is not found"}
        
        self.users.remove(target_user)

        return {
            "success": True,
            "message": "The user is successfully deleted"
        }


    def get_user_by_id(self, user_id: int) -> User | None:
        """The method searches for a user and returns it if it is found, otherwise returns None"""

        for user in self.users:
            if user.id == user_id:
                return user
        
        return None
    

    def get_available_user_roles(self) -> list:
        
        return AVAILABLE_ROLES
    

    def get_all_users(self) -> list:
        
        users = []

        for user in self.users:
            
            combined_fields = {
                "id": user.id,
                "name": user.name,
                "role": user.role,
                "responsible_cages": user.responsible_cages,
                "shift_is_active": user.shift_is_active
            }

            users.append(combined_fields)
        
        return users

    #----------- 


    # ----- Section logic -----
    def add_new_section(self, section_name: str, executor: User):
        """The method creates a new section"""
        
        if not self.is_authorised(executor, "add"):
            return {"success": False, "message": "Permission denied"}
        
        new_section = ZooSection(section_name)

        self.zoo.sections.append(new_section)

        return {
            "success": True,
            "message": "The section is successfully created",
            "zoo_section": new_section
        }
    

    def edit_section(self, section_id: int, parameters_to_update: dict, executor: User):
        """The method finds the section by its ID and edits it by the specified parameters"""
        
        if not self.is_authorised(executor, 'edit_section'):
            return {"success": False, "message": "Permission denied"}
        
        target_section = self.get_section_by_id(section_id)

        if not target_section:
            return {"success": False, "message": "The section is not found"}
        
        for key, value in parameters_to_update.items():
            if key == 'id':
                continue

            if key in EDITABLE_FIELDS["section"]:
                setattr(target_section, key, value)
        
        return {
            "success": True,
            "message": "The section is successfully updated",
            "section": target_section
        }
        

    def delete_section(self, secton_id: int, executor: User) -> dict:
        """The method deletes the section if the section is found"""
        
        if not self.is_authorised(executor, 'delete_section'):
            return {"success": False, "message": "Permossion denied"}
        
        target_section = self.get_section_by_id(secton_id)

        if not target_section:
            return {"success": False, "message": "The section is not found"}
        
        self.zoo.sections.remove(target_section)

        return {
            "success": True, 
            "message": "The section is successfully deleted"
        }


    def get_section_by_id(self, section_id: int) -> ZooSection | None:
        """The method searches for a section and returns it if it is found, otherwise returns None"""

        for section in self.zoo.sections:
            if section.id == section_id:
                return section
        
        return None
    
    # -----------


    # ----- Cages logic -----

    def add_new_cage(self, section_id: int, executor: User) -> dict:
        """The metdod creates a new cage and adds it to the section"""
        
        if not self.is_authorised(executor, "add"):
            return {"success": False, "message": "Permission denied"}
        
        targer_secrtion = self.get_section_by_id(section_id)

        if not targer_secrtion:
            return {"success": False, "message": "The section is not found"}
        
        new_cage = Cage()

        targer_secrtion.cages.append(new_cage)

        return {
            "success": True,
            "message": "The cage is successfully created",
            "cage": new_cage
        }
    

    def edit_cage(self, cage_id: int, parameters_to_update: dict, executor: User):
        """The method finds the cage by its ID and edits it by the specified parameters"""
        
        if not self.is_authorised(executor, "edit"):
            return {"success": False, "message": "Permission denied"}
        
        target_cage = self.get_cage_by_id(cage_id)

        if not target_cage:
            return {"success": False, "message": "The cage is not found"}
        
        for key, value in parameters_to_update.items():
            if key == 'id':
                continue

            if key in EDITABLE_FIELDS["cage"]:
                setattr(target_cage['cage'], key, value)

        return {
            "success": True,
            "message": "The cage is successfully updated",
            "cage": target_cage
        }
    

    def delete_cage(self, cage_id: int, executor: User) -> dict:
        """The method deletes the cage if the section is found"""
        if not self.is_authorised(executor, 'delete_cage'):
            return {"success": False, "message": "Permission denied"}
        
        target_cage = self.get_cage_by_id(cage_id)

        if not target_cage:
            return {"success": False, "message": "The cage is not found"}
        
        if len(target_cage['cage'].animals) > 0:
            return {"success": False, "message": "Before deletion of the cage, please place animals into another cage"}
        
        target_cage['section'].cages.remove(target_cage["cage"])

        return {
            "success": True,
            "message": "The cage is successfully deleted",
            "cage": target_cage['cage']
        }
        

    def get_cage_by_id(self, cage_id: int) -> dict | None:
        """The method searches for a cage and returns it if it is found, otherwise returns None"""

        for section in self.zoo.sections:
            
            for cage in section.cages:
                
                if cage.id == cage_id:
                    return {"section": section, "cage": cage}
                
        return None
    

    def get_all_cage_ids(self) -> list[int]:
        """The method returns IDs of all cages from all sections"""

        ids = []

        for section in self.zoo.sections:

            for cage in section.cages:

                ids.append(cage.id)
        
        return ids
    
    # ----------


    # ----- Animals logic -----

    def add_new_animal(self, animal: Animal, cage_id: int, executor: User) -> dict:
        """The metdod creates a new animal and adds it to the cage"""
        
        if not self.is_authorised(executor, 'add_animal'):
            return {"success": False, "message": "Permisson denied"}

        cage = self.get_cage_by_id(cage_id)

        if not cage:
            return {"success": False, "message": "The cage is not found"}
        
        cage['cage'].add_animal_to_cage(animal)

        return {
            "success": True,
            "message": "The aninal is successfully added to the cage"
        }
    

    def edit_animal(self, animal_id: int, parameters_to_update: dict, executor: User):
        """The method finds the animal by its ID and edits it by the specified parameters"""
        
        if not self.is_authorised(executor, "edit"):
            return {"success": False, "message": "Permission denied"}
        
        target_animal = self.get_animal_by_id(animal_id)

        if not target_animal:
            return {"success": False, "message": "The animal is not found"}
        
        for key, value in parameters_to_update.items():
            if key == 'id':
                continue

            if key in EDITABLE_FIELDS["animal"]:
                setattr(target_animal['animal'], key, value)
        
        return {
            "success": True,
            "message": "The animal is successfully updated",
            "animal": target_animal["animal"]
        }

    
    def delete_animal(self, animal_id: int, executor: User):
        """The method deletes the animal if the section is found"""

        if not self.is_authorised(executor, 'delete_animal'):
            return {"success": False, "message": "Permission denied"}
        
        target_animal = self.get_animal_by_id(animal_id)

        if not target_animal:
            return {"success": False, "message": "The animal is not found"}
        
        target_animal['cage'].animals.remove(target_animal['animal'])

        return {
            "success": True,
            "message": "The animal is successfully deleted"
        }
        

    def get_animal_by_id(self, animal_id: int) -> dict | None:
        """The method searches for aт animal and returns it if it is found, otherwise returns None"""

        for section in self.zoo.sections:

            for cage in section.cages:

                for animal in cage.animals:

                    if animal_id == animal.id:

                        return {
                            "cage": cage,
                            "animal": animal
                        }
                    
        return None







    



    
