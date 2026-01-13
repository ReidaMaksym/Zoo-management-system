from openpyxl import load_workbook, Workbook
from src.zoo_manager import ZooManager
from src.user import User
from src.section import ZooSection


FIELDS_WITH_LIST_TYPE = ['responsible_cages', 'cages', 'animals']

def get_data_from_sheet(sheet_name: str, work_book: Workbook) -> list:

    if sheet_name not in work_book.sheetnames:
        print(f"The sheet '{sheet_name}' doesn't exist")
        return []
    
    work_sheet = work_book[sheet_name]

    entities = []

    for i in range(2, work_sheet.max_row + 1):

        new_entity = {}

        for j in range(1, work_sheet.max_column + 1):

            key_name = work_sheet.cell(row=1, column=j).value
            cell_value = work_sheet.cell(row=i, column=j).value

            # print(f"key_name: {key_name}, cell_value: {cell_value}, type: {type(cell_value)}")
            # print("\n")

            # if key_name in FIELDS_WITH_LIST_TYPE:
            #     new_entity[key_name] = []
            
            # else:
            new_entity[key_name] = cell_value
        
        # print(f"NEW ENTITY: {new_entity}")

        try:
            entities.append(new_entity)
        except UnboundLocalError:
            print(f"The sheet '{sheet_name}' is empty, add the data first")
            return []

    return entities


# def create_users_from_list(user_list: list[dict], zoo_manager: ZooManager):
    
#     for user in user_list:

#         name = user['name']
#         role = user['role']
#         responsible_cages = user['responsible_cages']
#         shift_is_active = user['shift_is_active']

#         new_user = User(name, role, responsible_cages, shift_is_active)
#         zoo_manager.users.append(new_user)

def get_users_with_associated_cages(users_list: list) -> list:
    
    result = []

    for user in users_list:

        user_id = user['id']

        cages = user['responsible_cages']

        if cages == '' or cages is None:
            cages = []
        
        else:
            cages = cages.split(";")

            cages.remove('')

            cages = list(map(int, cages))
        
        entry = {
            "user_id": user_id,
            "cages": cages
        }

        result.append(entry)
    
    return result


def get_sections_with_associated_cages(sections_list: list):

    result = []

    for section in sections_list:

        section_id = section['id']

        cages = section['cages']

        print(f"cages: {cages}")

        if cages == '' or cages is None:
            cages = []
        
        else:
            cages = cages.split(";")

            cages.remove('')

            cages = list(map(int, cages))

        entry = {
            "section_id": section_id,
            "cages": cages
        }

        result.append(entry)

    return result


        

# def create_sections_from_list(sections_list: list, zoo_manager: ZooManager):
    
#     for section in sections_list:

#         name = section['name']
#         cages = section['cages']

#         new_section = ZooSection(name, cages)

#         zoo_manager.zoo.sections.append(new_section)

    

def save_users_to_file(sheet_name: str, work_book: Workbook, data: list[User], file_path: str):

    # if sheet_name not in work_book.sheetnames:
    #     print(f"The sheet '{sheet_name}' doesn't exist")
    #     return []

    work_sheet = work_book[sheet_name]

    formatted_data = [
        ['id', 'name', 'role', 'responsible_cages', 'shift_is_active']
    ]

    for user in data:
        new_row = [user.id, user.name, user.role, user.responsible_cages, user.shift_is_active]

        formatted_data.append(new_row)

    
    print(f"FORMATTED DATA: {formatted_data}")


    work_sheet.delete_rows(1, work_sheet.max_row)

    for row_index, row_data in enumerate(formatted_data, start=1):
        print(row_data)

        for index, item in enumerate(row_data, start=1):

            if item == []:
                work_sheet.cell(row= row_index, column= index, value=' ')
            else:
                work_sheet.cell(row= row_index, column= index, value=item)
    
    work_book.save(file_path)
    








        




