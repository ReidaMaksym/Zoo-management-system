from src.zoo_manager import ZooManager, AVAILABLE_ROLES
from src.user import User


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

        print("-------------------------------")

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
    

    def _prepare_fields_for_user_edit(self, user: User):

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
                
                print(ids_list)

                existing_cage_ids = self.zoo_manager.get_all_cage_ids()

                for id in ids_list:

                    if id not in existing_cage_ids:

                        print(f"The ID '{id}' does not exists and will be ignored")
                        ids_list.remove(id)
                
                fields_to_update['responsible_cages'] = ids_list

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
    

    def handle_choise(self, user_choice: int):
        
        if user_choice == 1:
            
            user_name = input("Enter the user name, for example: 'Maksym Reida': ")
            user_role = input("Enter the role of the user ('manager', 'caretaker'): ").lower()

            available_user_roles = self.zoo_manager.get_available_user_roles()

            while user_role not in available_user_roles:
                print("Sorry, you entered an invalid role")
                user_role = input("Enter the role of the user ('manager', 'caretaker'): ").lower()


            new_user = self.zoo_manager.add_new_user(name=user_name, role=user_role, executor=self.executor)

            print(new_user['message'])

        elif user_choice == 2:
            
            # users = self.zoo_manager.get_all_users()
            # print(users)

            # for user in users:

            #     print("----------")
            #     print(f"{user['name']}, ID = {user['id']}")
            #     print(f"Role - {user['role']}")
            #     print(f"Responsible cages - {user['responsible_cages']}")
            #     print(f"Shift is active - {user['shift_is_active']}")
            #     print("----------")
            
            while True:
                try:
                    user_id = int(input("Enter the ID of the user you want to update: "))
                    break
                except ValueError:
                    print("You ented invalid ID, please enter valid ID")
                    user_id = int(input("Enter the ID of the user you want to update: "))

            user = self.zoo_manager.get_user_by_id(user_id)

            print(user)

            if not user:
                print(f"The user with ID={user_id} is not found")
                return
            
            fields_to_update = self._prepare_fields_for_user_edit(user)

            updated_user = self.zoo_manager.edit_user(user_id, self.executor, fields_to_update)

            print(updated_user)






            
            
            

        
