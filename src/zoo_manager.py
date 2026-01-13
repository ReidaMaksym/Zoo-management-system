from src.animal import Animal, Mammal, Bird, Reptile
from src.cage import Cage
from src.section import ZooSection
from src.user import User
from src.zoo import Zoo
from typing import TypedDict

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

AVAILABLE_ROLES_FOR_FILE = ['owner' ,'manager', 'caretaker']


EDITABLE_FIELDS = {
    "user": ['name', 'role', 'responsible_cages', 'shift_is_active'],
    "section": ["name", "cages"],
    "cage": ['animals'],
    "animal": ['name', 'age', 'fur_color', 'wing_span', 'can_fly']
}


FIELDS_TO_CREATE_ANIMAL = {
    'mammal': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('animal_type', 'Animal Type'),
        ('species', 'Species'),
        ('breed', 'Breed'),
        ('fur_color', 'Fur Color')
    ],
    'bird': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('animal_type', 'Animal Type'),
        ('wing_span', 'Wing span'),
        ('can_fly', 'Can fly')
    ],
    'reptile': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('animal_type', 'Animal Type'),
        ('is_venomus', 'Is venomus')
    ]
}


FIELDS_TO_EDIT_ANIMAL = {
    'mammal': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('fur_color', 'Fur Color')
    ],
    'bird': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('wing_span', 'Wing span'),
        ('can_fly', 'Can fly')
    ],
    'reptile': [
        ('name', 'Name'),
        ('age', 'Age')
    ]    

}


ANIMAL_TYPES = ['mammal', 'bird', 'reptile']


class CageSearchResult(TypedDict):

    section: ZooSection
    cage: Cage


class AnimalSearchResult(TypedDict):

    cage: Cage
    animal: Animal


class AnimalFactory:

    _regestry = {
        'mammal': Mammal,
        'bird': Bird,
        'reptile': Reptile
    }

    @classmethod
    def create_animal(cls, animal_type, data: dict):

        try:
            animal_class = cls._regestry[animal_type]
            
            return {
                "success": True,
                "message": f"The animal with type '{animal_type}' is created",
                "animal": animal_class(**data)
            }

        except KeyError:
            return {"success": False, "message": f"The type '{animal_type}' doesn't exist"}
        

class ZooManager:

    def __init__(self, zoo: Zoo) -> None:
        self.zoo = zoo
        self.users = []

    
    def is_authorised(self, executor: User, operation: str) -> bool:
        """The method determines whether the user is allowed to make an operation or not"""
        return executor.role in AUTHORISED_ROLES.get(operation, [])


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
    

    def create_new_user_from_file(self, users_from_file: list[dict]):
        
        if len(users_from_file) == 0:
            return {"success": False, "message": "There are no users in the file"}
        
        
        for user in users_from_file:

            if user['role'] not in AVAILABLE_ROLES_FOR_FILE:
                print(f"The user '{user['name']}' is ignorred because role '{user['role']}' is not valid")
                continue

            if len(user["name"]) == 0:
                print(f"The user with ID: {user['id']} doesn't have a name, they will be ignorred")
                continue

            name = user["name"]
            role = user["role"]
            shift = user["shift_is_active"]

            new_user = User(name, role, shift_is_active=shift)

            self.users.append(new_user)
        
        return {
            "success": True,
            "message": "The users are successfully created"
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
    

    def create_new_sections_from_file(self, sections_list: list):

        if len(sections_list) == 0:
            return {"success": False, "message": "There are no sections in the file"}
        
        for section in sections_list:

            section_name = section['name']

            if len(section_name) == 0:
                print(f"The section name can not be empty, the section with ID: {section['id']} is ignorred")
                continue

            new_section = ZooSection(section_name)

            self.zoo.sections.append(new_section)

        return {
            "success": True,
            "message": "The sections are successfully created"
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

                if key == 'cages':
                    
                    cage_with_section = self._get_cage_and_section_objects_from_cage_id(value)

                    new_cage_list = self._reasign_cage_to_another_section(target_section, cage_with_section)

                    setattr(target_section, key, new_cage_list)

                else:
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
        
        if len(target_section.cages) > 0:
            return {"success": False, "message": f"The section: '{target_section.name}' has attached cages. Reassign the cages first"}
        
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
    

    def _reasign_cage_to_another_section(self, target_section: ZooSection, new_cage_list: list[CageSearchResult]) -> list[Cage]:
        """The method receives as a parameter the section that is being edited (target_section) and the list of cages with
        their sections. If the cage belongs not to target_section, it removes from section that it belongs. The method returns the
        new list of cages for target_section"""
       
        result = []
        
        for item in new_cage_list:

            if target_section.id != item["section"].id:

                item["section"].cages.remove(item["cage"])

            result.append(item["cage"])
        
        return result            

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

                if key == 'animals':
                    
                    animals_with_cage = self._get_animal_and_cage_object_from_animal_ids(value)

                    new_animal_list = self._reasing_animal_to_another_cage(target_cage["cage"], animals_with_cage)
                
                    setattr(target_cage["cage"], key, new_animal_list)
                
                else:
                    setattr(target_cage['cage'], key, value)

        return {
            "success": True,
            "message": "The cage is successfully updated",
            "cage": target_cage["cage"]
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
        

    def get_cage_by_id(self, cage_id: int) -> CageSearchResult | None:
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


    def find_existing_cage_ids_in_list(self, ids: list[int]) -> list[int]:
        """The method receives as a parameter a list of cage ids, loops through this list and gets only existing ids
        and writes them into new list and returns it"""

        all_cage_ids = self.get_all_cage_ids()

        real_ids = []

        for id in ids:
            
            if id in all_cage_ids:

                real_ids.append(id)
        
        return real_ids
    

    def _get_cage_and_section_objects_from_cage_id(self, ids: list[int]) -> list[CageSearchResult]:
        """The method receives as a parameter the list of Cage ids, then finds the cage by id and 
        appends it to a new list and then this list is returned"""
        
        cages_objects = []

        for id in ids:

            cage = self.get_cage_by_id(id)

            if cage != None:
                cages_objects.append(cage)
        
        return cages_objects
    

    def _reasing_animal_to_another_cage(self, target_cage: Cage, animals_with_cage: list[AnimalSearchResult]) -> list[Animal]:
        
        new_animal_list = []

        for item in animals_with_cage:

            if target_cage.id != item["cage"].id:

                item["cage"].animals.remove(item["animal"])
            
            new_animal_list.append(item["animal"])
        
        return new_animal_list
            
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
            "message": "The animal is successfully added to the cage"
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
        

    def get_animal_by_id(self, animal_id: int) -> AnimalSearchResult | None:
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
    

    def get_all_animals_ids(self) -> list[int]:

        animal_ids = []

        for section in self.zoo.sections:

            for cage in section.cages:

                for animal in cage.animals:

                    animal_ids.append(animal.id)
        
        return animal_ids
    

    def find_existing_animal_ids_in_list(self, animal_ids: list[int]) -> list[int]:

        all_animal_ids = self.get_all_animals_ids()

        existing_ids = []

        if len(animal_ids) == 0:
            return []

        for animal_id in animal_ids:

            if animal_id in all_animal_ids:

                existing_ids.append(animal_id)
        
        return existing_ids
    

    def _get_animal_and_cage_object_from_animal_ids(self, aninal_ids: list[int]) -> list[AnimalSearchResult]:
        
        animal_with_cage = []

        for id in aninal_ids:

            animal = self.get_animal_by_id(id)

            if animal != None:

                animal_with_cage.append(animal)
        
        return animal_with_cage


    def get_fields_to_edit_animal_by_animal_type(self, animal_type: str) -> list[tuple] | None:

        return FIELDS_TO_EDIT_ANIMAL.get(animal_type, None)
        

    
