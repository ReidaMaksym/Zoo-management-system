AUTHORISED_ROLES = {
    'add': ['owner', 'manager'],
    'edit': ['owner', 'manager', 'caretaker'],
    'delete': ['owner'],
    'edit_section': ['owner', 'manager'],
    'delete_section': ['owner', 'manager'],
    'delete_cage': ['owner', 'manager'],
    'add_animal': ['owner', 'manager', 'caretaker'],
    'delete_animal': ['owner', 'manager', 'caretaker']
}

AVAILABLE_ROLES = ['manager', 'caretaker']

AVAILABLE_ROLES_FOR_FILE = ['owner' ,'manager', 'caretaker']

EDITABLE_FIELDS = {
    "user": ['name', 'role', 'responsible_cages', 'shift_is_active'],
    "section": ["name", "cages"],
    "cage": ['animals'],
    "animal": ['name', 'age', 'fur_color', 'wing_span', 'can_fly']
}

FIELDS_TO_CREATE_ANIMAL = {
    'mammal': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('animal_type', 'Animal Type'),
        ('species', 'Species'),
        ('breed', 'Breed'),
        ('fur_color', 'Fur Color')
    ],
    'bird': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('animal_type', 'Animal Type'),
        ('wing_span', 'Wing span'),
        ('can_fly', 'Can fly')
    ],
    'reptile': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('animal_type', 'Animal Type'),
        ('is_venomus', 'Is venomus')
    ]
}

FIELDS_TO_EDIT_ANIMAL = {
    'mammal': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('fur_color', 'Fur Color')
    ],
    'bird': [
        ('name', 'Name'),
        ('age', 'Age'),
        ('wing_span', 'Wing span'),
        ('can_fly', 'Can fly')
    ],
    'reptile': [
        ('name', 'Name'),
        ('age', 'Age')
    ]    

}

ANIMAL_TYPES = ['mammal', 'bird', 'reptile']