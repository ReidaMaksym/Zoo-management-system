from src.animal import Animal, Mammal, Reptile
from src.section import ZooSection
from src.cage import Cage
from src.zoo import Zoo
from src.zoo_manager import ZooManager, AnimalFactory
from src.user import User
from ui.menu import Menu
from openpyxl import load_workbook, Workbook
import data.read_write_excel as file_funk


zoo = Zoo("Test zoo")

zoo_manager = ZooManager(zoo)

file = 'data/zoo_data.xlsx'

wb = load_workbook(file)

# owner = User("Maksym owner", "owner")
# zoo_manager.users.append(owner)

users_from_file = file_funk.get_data_from_sheet('users', wb)

users_with_associated_cages = file_funk.get_users_with_associated_cages(users_from_file)

print(f"users_with_associated_cages: {users_with_associated_cages}")

# print(f"users_from_file: {users_from_file}")

zoo_manager.create_new_user_from_file(users_from_file)

# print(f"zoo_manager.users: {zoo_manager.users}")

sections_from_file = file_funk.get_data_from_sheet('sections', wb)

print(f"sections_from_file: {sections_from_file}")

# file_funk.create_sections_from_list(sections_from_file, zoo_manager)
zoo_manager.create_new_sections_from_file(sections_from_file)

# print(f"Zoo Sections: {zoo_manager.zoo.sections}")

sections_with_associated_cages = file_funk.get_sections_with_associated_cages(sections_from_file)

print(f"sections_with_associated_cages: {sections_with_associated_cages}")

# print(zoo_manager.users)

owner = zoo_manager.users[0]

# zoo_manager.add_new_section("Section 1", owner)
# zoo_manager.add_new_section("Section 2", owner)
# zoo_manager.add_new_section("Section 3", owner)

# zoo_manager.add_new_cage(1, owner)
# zoo_manager.add_new_cage(1, owner)
# zoo_manager.add_new_cage(1, owner)

# zoo_manager.add_new_cage(2, owner)
# zoo_manager.add_new_cage(2, owner)
# zoo_manager.add_new_cage(2, owner)

# zoo_manager.add_new_cage(3, owner)
# zoo_manager.add_new_cage(3, owner)
# zoo_manager.add_new_cage(3, owner)

# reptile1 = Reptile(name="reptile 1", age='1', animal_type="reptile", is_venomus='False')
# reptile2 = Reptile(name="reptile 2", age='1', animal_type="reptile", is_venomus='False')
# mammal1 = Mammal(name= 'mammal 1', age= '2', animal_type='mammal', species='test species', breed='test breed', fur_color='test fur color')

# reptile3 = Reptile("reptile 3", '1', "reptile", False)
# reptile4 = Reptile("reptile 4", '1', "reptile", False)
# reptile5 = Reptile("reptile 5", '1', "reptile", False)
# reptile6 = Reptile("reptile 6", '1', "reptile", False)

# zoo_manager.add_new_animal(reptile1, 1, owner)
# zoo_manager.add_new_animal(reptile2, 1, owner)

# zoo_manager.add_new_animal(reptile3, 1, owner)

# zoo_manager.add_new_animal(mammal1, 2, owner)

# zoo_manager.add_new_animal(reptile5, 2, owner)
# zoo_manager.add_new_animal(reptile6, 2, owner)



# caretaker1 = User("Maksym caretaker", "caretaker")
# zoo_manager.users.append(caretaker1)

active_user = owner
menu = Menu(zoo_manager, active_user)

menu.print_menu()

# menu.executor = caretaker1

# user_choice = menu.get_user_menu_choice()
# result = menu.handle_choise(user_choice)




while True:

    # user_choise = input("Select operation: ")
    user_choice = menu.get_user_menu_choice()
    if user_choice == 0:
        file_funk.save_users_to_file('users', wb, zoo_manager.users, file)
        break
    result = menu.handle_choise(user_choice)
