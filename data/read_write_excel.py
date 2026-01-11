from openpyxl import load_workbook, Workbook
from src.zoo_manager import ZooManager
from src.user import User

wb = load_workbook('data/zoo_data.xlsx')

# sheet = wb.active

# print(sheet.title)

# print(wb.sheetnames)

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

            new_entity[key_name] = cell_value
        
        # print(f"NEW ENTITY: {new_entity}")

        try:
            entities.append(new_entity)
        except UnboundLocalError:
            print(f"The sheet '{sheet_name}' is empty, add the data first")
            return []

    return entities


print(get_data_from_sheet('users', wb))

def create_users_from_list(user_list: list, zoo_manager: ZooManager):
    
    for user in user_list:

        name = user['name']
        role = user['role']

        new_user = User(name, role)
        zoo_manager.users.append(new_user)

    

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

        # for field in new_row:
        #     if field == []:
        #         formatted_data.append(' ')
        #     else:
        #         formatted_data.append(field)

        formatted_data.append(new_row)

    
    print(f"FORMATTED DATA: {formatted_data}")

    start_column = 1
    start_row = 1

    work_sheet.delete_rows(1, work_sheet.max_row)

    for row_index, row_data in enumerate(formatted_data, start=1):
        print(row_data)

        for index, item in enumerate(row_data, start=1):

            if item == []:
                work_sheet.cell(row= row_index, column= index, value=' ')
            else:
                work_sheet.cell(row= row_index, column= index, value=item)

    # for index, item in enumerate(formatted_data):

    #     for j in range(1, 6):

    #         work_sheet.cell(row=start_row + j, column=start_column + j, value=item)



    
    # for row in formatted_data:

    #     work_sheet.append(row)
    
    work_book.save(file_path)
    








        




