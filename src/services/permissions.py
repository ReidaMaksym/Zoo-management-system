from src.domain.user import User
from src.config.constants import Constants


class PermissionService:

    def is_authorised(self, executor: User, operation: str) -> bool:
        """The method determines whether the user is allowed to make an operation or not"""
        return executor.role in Constants.AUTHORISED_ROLES.get(operation, [])

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
    

