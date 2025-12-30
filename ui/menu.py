from src.zoo_manager import ZooManager, AVAILABLE_ROLES
from src.user import User
from src.section import ZooSection
from src.cage import Cage

MESSAGE_FOR_USER_TO_GET_ID = {
    'user': {
        'positive': 'Enter the ID of the user: ',
        'negative': 'You ented invalid ID, please enter valid user ID'
    },

    'section': {
        'positive': 'Enter the ID of the section: ',
        'negative': 'You ented invalid ID, please enter valid section ID'
    },

    'cage': {
        'positive': 'Enter the ID of the cage: ',
        'negative': 'You ented invalid ID, please enter valid cage ID'
    }
}


class Menu():

    def __init__(self, zoo_manager: ZooManager, executor: User) -> None:
        self.zoo_manager = zoo_manager
        self.executor = executor  


    def print_menu(self) -> None:
        print("==============================")

        print("Enter '1' to create a new user;")
        print("Enter '2' to edit the user;")
        print("Enter '3' to delete the user;")

        print("-------------------------------")

        print("Enter '4' to add a new section;")
        print("Enter '5' to edit the section;")
        print("Enter '6' to delete the section;")

        print("-------------------------------")

        print("Enter '7' to add a new cage;")
        print("Enter '8' to edit the cage;")
        print("Enter '9' to delete the cage;")

        print("-------------------------------")

        print("Enter '10' to add a new animal;")
        print("Enter '11' to edit the animal;")
        print("Enter '12' to delete the animal;")
        print("Enter '0' to close the system;")

        print("==============================")


    def get_user_menu_choice(self) -> int:
        user_chose = -1
        while True:
            try:
                user_chose = int(input("Enter your choise: "))
                break
            except ValueError:
                print("Enter corrent option from the menu")
                self.print_menu()
                        
        return user_chose
    

    # ----- User logic -----

    def _prepare_fields_for_user_edit(self, user: User) -> dict:

        fields_to_update = {}

        print(f"1. Name: {user.name}")
        print(f"2. Role: {user.role}")
        print(f"3. Responsible cages: {user.responsible_cages}")
        print(f"4. Shift is active: {user.shift_is_active}")

        while True:

            user_choice = input("Enter a number for a field you want to update, enter '0' to finish: ")
            
            if user_choice == '1':

                new_name = input("Enter a new name: ")
                fields_to_update['name'] = new_name

            elif user_choice == '2':

                new_role = input("Enter a new role (namager of caretaker): ").lower()

                while new_role not in AVAILABLE_ROLES:
                    print("You entered invalid role")
                    new_role = input("Enter a new role (namager of caretaker): ").lower()
                
                fields_to_update['role'] = new_role
            
            elif user_choice == '3':
                
                user_input = input("Enter a sequence of IDs separated by spaces: ")

                numbers_as_strings = user_input.split()

                ids_list = []

                for id in numbers_as_strings:
                    try:
                        ids_list.append(int(id))
                    except ValueError:
                        print(f"Skipping an invalid ID of - {id}")
                
                if len(ids_list) > 0:

                    existing_cage_ids = self.zoo_manager.get_all_cage_ids()
                    unique_ids = list(set(ids_list))

                    for id in unique_ids:

                        if id not in existing_cage_ids:

                            print(f"The ID '{id}' does not exists and will be ignored")
                            unique_ids.remove(id)
                    
                    fields_to_update['responsible_cages'] = unique_ids
                
                else:
                    print("Valid IDs are not found and the current list is not changed")
                    fields_to_update['responsible_cages'] = user.responsible_cages

            elif user_choice == '4':
                
                user_input = input("Enter 'True' for the active shift, or enter 'False' for finished shift: ").lower()

                if user_input == 'true':
                    fields_to_update['shift_is_active'] = True
                else:
                    fields_to_update['shift_is_active'] = False
                
            elif user_choice == '0':
                return fields_to_update
            
            else:
                print("Sorry, no such field")
    

    def _get_id_from_input(self, message: dict) -> int:

        while True:
            try:
                id = int(input(message['positive']))
                break
            except ValueError:
                print(message['negative'])
        
        return id


    def create_new_user(self):

        user_name = input("Enter the user name, for example: 'Maksym Reida': ")
        user_role = input("Enter the role of the user ('manager', 'caretaker'): ").lower()

        available_user_roles = self.zoo_manager.get_available_user_roles()

        while user_role not in available_user_roles:
            print("Sorry, you entered an invalid role")
            user_role = input("Enter the role of the user ('manager', 'caretaker'): ").lower()


        new_user = self.zoo_manager.add_new_user(name=user_name, role=user_role, executor=self.executor)

        print(new_user['message'])


    def edit_user(self):

            user_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID["user"])

            user = self.zoo_manager.get_user_by_id(user_id)

            if not user:
                print(f"The user with ID={user_id} is not found")
                return
            
            fields_to_update = self._prepare_fields_for_user_edit(user)

            updated_user = self.zoo_manager.edit_user(user_id, self.executor, fields_to_update)

            print(updated_user)
    

    def delete_user(self):

        user_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID['user'])

        delete_user = self.zoo_manager.delete_user(user_id, self.executor)

        print(delete_user['message'])


    # ----- Section logic ------

    def create_new_section(self):
        
        section_name = input("Enter a section name: ")

        new_section = self.zoo_manager.add_new_section(section_name, self.executor)

        print(new_section['message'])
    

    def _prepare_fields_for_section_edit(self, section: ZooSection) -> dict:
        
        fields_to_update = {}

        print(f'1. Name: {section.name}')
        print(f"2. Cages: {section.cages}")

        while True:

            user_choice = input("Enter a number for a field you want to update, enter '0' to finish: ")

            if user_choice == '1':

                new_name = input("Enter a new secton name: ")

                if len(new_name) == 0:
                    print("The name is not changed")
                
                fields_to_update['name'] = new_name
            
            elif user_choice == '2':

                user_iptut = input("Enter cages ids separated by space: ")

                ids_as_string = user_iptut.split()

                ids_as_int = []

                for number in ids_as_string:

                    try:
                        ids_as_int.append(int(number))
                    except ValueError:
                        print(f"The provided ID = '{number}' is not an integer number and it will be ignored")

                if len(ids_as_int) == 0:
                    fields_to_update['cages'] = section.cages
                    continue
                
                unique_ids = list(set(ids_as_int))
                existing_ids = self.zoo_manager.find_existing_cage_ids_in_list(unique_ids)

                if len(existing_ids) == 0:
                    fields_to_update['cages'] = section.cages
                    continue

                fields_to_update['cages'] = existing_ids
                
            elif user_choice == '0':
                return fields_to_update
            
            else:
                print("Sorry, no such field")


    def edit_section(self):

        section_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID["section"])

        section = self.zoo_manager.get_section_by_id(section_id)

        if not section:
            print(f"The section with ID = '{section_id}' is not found")
            return
        
        parameters_to_update = self._prepare_fields_for_section_edit(section)

        updated_section = self.zoo_manager.edit_section(section.id, parameters_to_update, self.executor)
        
        print(updated_section)
    

    def delete_section(self):

        section_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID["section"])

        delete_section = self.zoo_manager.delete_section(section_id, self.executor)

        print(delete_section)


    # ----- Cage logic -----

    def create_new_cage(self):

        section_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID["section"])

        new_cage = self.zoo_manager.add_new_cage(section_id, self.executor)

        print(new_cage)

    
    def _prepare_fields_for_cage_edit(self, cage: Cage):

        fields_to_update = {}

        print(f"1. Animals: {cage.animals}")

        while True:

            user_choice = input("Enter a number for a field you want to update, enter '0' to finish: ")

            if user_choice == '1':
                
                user_input = input("Enter animals IDs separated by space: ")

                ids_as_strings = user_input.split()

                ids_as_int = []

                for number in ids_as_strings:

                    try:
                        ids_as_int.append(int(number))
                    except ValueError:
                        print(f"The provided ID = '{number}' is not an integer number and it will be ignored")
                
                if len(ids_as_int) == 0:
                    fields_to_update['animals'] = cage.animals
                    continue

                unique_ids = list(set(ids_as_int))
                existing_ids = self.zoo_manager.find_existing_animal_ids_in_list(unique_ids)

                if len(existing_ids) == 0:
                    fields_to_update["animals"] = cage.animals
                    continue

                fields_to_update["animals"] = existing_ids

            elif user_choice == '0':
                return fields_to_update
            
            else:
                print("Sorry, no such field")
    

    def edit_cage(self):

        cage_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID["cage"])

        cage = self.zoo_manager.get_cage_by_id(cage_id)

        if not cage:
            print(f"The cage with ID = '{cage_id}' is not found")
            return

        parameters_to_update = self._prepare_fields_for_cage_edit(cage["cage"])

        updated_cage = self.zoo_manager.edit_cage(cage["cage"].id, parameters_to_update, self.executor)

        print(updated_cage)


    def delete_cage(self):

        cage_id = self._get_id_from_input(MESSAGE_FOR_USER_TO_GET_ID["cage"])

        delete_cage = self.zoo_manager.delete_cage(cage_id, self.executor)

        print(delete_cage)


    def invalid_choise(self):
        print("You entered unavailable option")


    def handle_choise(self, user_choice: int):

        available_choices = {
            1: self.create_new_user,
            2: self.edit_user,
            3: self.delete_user,

            4: self.create_new_section,
            5: self.edit_section,
            6: self.delete_section,

            7: self.create_new_cage,
            8: self.edit_cage,
            9: self.delete_cage
        }

        available_choices.get(user_choice, self.invalid_choise)()
    
