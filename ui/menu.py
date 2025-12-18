from src.zoo_manager import ZooManager
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
        user_chose = 0
        while True:
            try:
                user_chose = int(input("Enter your choise: "))
                break
            except ValueError:
                print("Enter corrent option from the menu")
                self.print_menu()
                        
        return user_chose
    

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
        
