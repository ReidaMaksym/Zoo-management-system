from src.domain.animal import Animal, Mammal, Reptile
from src.domain.section import ZooSection
from src.domain.cage import Cage
from src.domain.zoo import Zoo
from src.zoo_manager import ZooManager, AnimalFactory
from src.domain.user import User
from ui.menu import Menu
from openpyxl import load_workbook, Workbook
import data.read_write_excel as file_funk


zoo = Zoo("Test zoo")

zoo_manager = ZooManager(zoo)

file = 'data/zoo_data.xlsx'

wb = load_workbook(file)

users_from_file = file_funk.get_data_from_sheet('users', wb)

users_with_associated_cages = file_funk.get_users_with_associated_cages(users_from_file)

zoo_manager.create_new_user_from_file(users_from_file)


sections_from_file = file_funk.get_data_from_sheet('sections', wb)

zoo_manager.create_new_sections_from_file(sections_from_file)

sections_with_associated_cages = file_funk.get_sections_with_associated_cages(sections_from_file)


cages_from_file = file_funk.get_data_from_sheet('cages', wb)

cages = zoo_manager.create_new_cages_from_file(cages_from_file)




cages_with_associated_animals = file_funk.get_cages_with_associated_animals(cages_from_file)

# print(f"cages_with_associated_animals: {cages_with_associated_animals}")

animals_from_file = file_funk.get_data_from_sheet('animals', wb)
# print(f"animals_from_file: {animals_from_file}")

animals = zoo_manager.create_new_animals_from_file(animals_from_file)

for item in cages_with_associated_animals:

    target_cage = zoo_manager.get_cage_by_id_from_temp_storage(item['cage_id'])

    animal_objects = zoo_manager.get_animals_from_temp_storage_by_id(item['animals'])

    if target_cage is not None:

        zoo_manager.edit_temp_cage(target_cage, {'animals': animal_objects})

print(zoo_manager.temp_storage['cages'])

for item in sections_with_associated_cages:

    print(item)

    target_section = zoo_manager.get_section_by_id_from_temp_storage(item['section_id'])

    cages_list = []

    for cage_id in item['cages']:
        
        cage = zoo_manager.get_cage_by_id_from_temp_storage(cage_id)

        cages_list.append(cage)

    if target_section is not None:

        zoo_manager.edit_temp_section(target_section, cages_list)
    
    zoo_manager.zoo.sections.append(target_section)

# print(zoo_manager.zoo.sections)

for item in users_with_associated_cages:

    print(item)

    target_user = zoo_manager.get_user_by_id(item['user_id'])

    cages_list = []

    for cage_id in item['cages']:

        cage = zoo_manager.get_cage_by_id_from_temp_storage(cage_id)

        cages_list.append(cage)
    
    if target_user is not None:

        zoo_manager.edit_temp_user(target_user, cages_list)



owner = zoo_manager.users[0]

active_user = owner
menu = Menu(zoo_manager, active_user)

menu.print_menu()



while True:

    # user_choise = input("Select operation: ")
    user_choice = menu.get_user_menu_choice()
    if user_choice == 0:
        file_funk.save_users_to_file('users', wb, zoo_manager.users, file)
        break
    result = menu.handle_choise(user_choice)
