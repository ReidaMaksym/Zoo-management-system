from src.animal import Animal, Mammal, Reptile
from src.section import ZooSection
from src.cage import Cage
from src.zoo import Zoo
from src.zoo_manager import ZooManager, AnimalFactory
from src.user import User
from ui.menu import Menu


zoo = Zoo("Test zoo")

zoo_manager = ZooManager(zoo)

owner = User("Maksym owner", "owner")
zoo_manager.users.append(owner)

zoo_manager.add_new_section("Section 1", owner)
zoo_manager.add_new_section("Section 2", owner)
zoo_manager.add_new_section("Section 3", owner)

zoo_manager.add_new_cage(1, owner)
zoo_manager.add_new_cage(1, owner)
zoo_manager.add_new_cage(1, owner)

zoo_manager.add_new_cage(2, owner)
zoo_manager.add_new_cage(2, owner)
zoo_manager.add_new_cage(2, owner)

zoo_manager.add_new_cage(3, owner)
zoo_manager.add_new_cage(3, owner)
zoo_manager.add_new_cage(3, owner)

reptile1 = Reptile(name="reptile 1", age='1', animal_type="reptile", is_venomus='False')
reptile2 = Reptile(name="reptile 2", age='1', animal_type="reptile", is_venomus='False')
# reptile3 = Reptile("reptile 3", '1', "reptile", False)
# reptile4 = Reptile("reptile 4", '1', "reptile", False)
# reptile5 = Reptile("reptile 5", '1', "reptile", False)
# reptile6 = Reptile("reptile 6", '1', "reptile", False)

zoo_manager.add_new_animal(reptile1, 1, owner)
zoo_manager.add_new_animal(reptile2, 1, owner)
# zoo_manager.add_new_animal(reptile3, 1, owner)
# zoo_manager.add_new_animal(reptile4, 2, owner)
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
        break
    result = menu.handle_choise(user_choice)























# manager1 = User("Maksym manager", "manager")
# manager2 = User("Maksym manager 2", "manager")
# caretaker1 = User("Maksym caretaker", "caretaker")


# zoo_manager.users.append(manager1)
# zoo_manager.users.append(manager2)
# zoo_manager.users.append(caretaker1)

# new_user = zoo_manager.add_new_user("New caretaker", "caretaker", manager1)

# print(zoo_manager.users)

# print(zoo.sections)

# print(zoo_manager.add_new_section("Section 1", owner, zoo))

# print(zoo.sections)

# print(zoo_manager.edit_section(1, {'name': "New section name", "cages": [1, 2, 4]}, manager1, zoo))

# print(zoo.sections)

# print(zoo_manager.delete_section(2, owner, zoo))

# print(zoo.sections)

# print(zoo_manager.add_new_cage(1, owner, zoo))

# print(zoo.sections)

# print(zoo_manager.edit_cage(1, {"animals": ['test1', 'test2']}, owner, zoo))

# print(zoo.sections)

# print(zoo_manager.delete_cage(1, owner, zoo))

# print(zoo.sections)

# lion = Mammal(
#     name="Simba",
#     age=5,
#     animal_type="mammal",
#     species="Panthera leo",
#     breed="African Lion",
#     fur_color="Golden"
# )

# print(zoo_manager.add_new_animal(lion, 1, caretaker1, zoo))

# print(zoo.sections)

# print(zoo_manager.edit_animal(1, {"name": "New Name"}, owner, zoo))

# print(zoo.sections)

# print(zoo_manager.delete_animal(2, owner, zoo))

# print(zoo.sections)





# section1 = ZooSection("Section 1")

# print(zoo_manager.edit_user(4, new_user['user'], {"name": "New name"}))


# print(owner.name)
# print(manager1.name)
# print(caretaker1.name)

# print(zoo_manager.delete_user(5, manager1))
# print(zoo_manager.users)





# cage1 = Cage()
# cage2 = Cage()

# woolf1 = Mammal("wool1", 2, "mammal", "test species", "test breed", "grey")

# cage1.add_animal_to_cage(woolf1)

# print(section1.get_all_cages())

# print(section1.get_cage_by_id(2))
