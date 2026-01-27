from src.domain.user import User
from src.services.permissions import PermissionService
from src.config.constants import Constants
from src.domain.cage import Cage

class UserService:

    def __init__(self, permissions: PermissionService) -> None:
        self.permissions = permissions
        self.users = []

    def add_new_user(self, name: str, role: str, executor: User) -> dict:
        """The method creates a new user"""

        if not self.permissions.is_authorised(executor, 'add'):
            return {"success": False, "message": "Permission denied"}
        
        if role not in self.get_available_user_roles():
            return {"success": False, "message": "Provided role does not exist"}
        
        new_user = User(name, role)
        self.users.append(new_user)

        return {
            "success": True,
            "message": "The user is successfully created",
            "user": new_user
        }
    

    def edit_user(self, user_id: int, executor: User, parameters_to_update: dict):
        """The method finds the user by its ID and edits it by the specified parameters"""
        
        if not self.permissions.is_authorised(executor, "edit"):
            return {"success": False, "message": "Permission denied"}

        editable_user = self.get_user_by_id(user_id)

        if not editable_user:
            return {"success": False, "message": "The user is not found"}
        
        if not self.permissions.can_edit_user(executor, editable_user):
            return {"success": False, "message": "Permission denied"}
        
        for key, value in parameters_to_update.items():
            if key == 'id':
                continue

            if key in Constants.EDITABLE_FIELDS["user"]:
                setattr(editable_user, key, value)
        
        return {
            "success": True,
            "message": "The user is successfully updated",
            "user": editable_user
        }
    

    def edit_temp_user(self, user: User, cages_list: list[Cage]):

        setattr(user, 'responsible_cages', cages_list)
    

    def delete_user(self, user_id: int, executor: User) -> dict:
        """The method deletes the user if the user is found"""
        
        if not self.permissions.is_authorised(executor, "delete"):
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
    

    def create_new_user_from_file(self, users_from_file: list[dict]):
    
        if len(users_from_file) == 0:
            return {"success": False, "message": "There are no users in the file"}
        
        
        for user in users_from_file:

            if user['role'] not in Constants.AVAILABLE_ROLES_FOR_FILE:
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
    

    def get_available_user_roles(self) -> list:
        
        return Constants.AVAILABLE_ROLES


