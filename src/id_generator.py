current_id = {}

def get_next_id(entity_type: str) -> int:
    """Generates a unique ID for a given entity type"""
    if entity_type not in current_id:
        current_id[entity_type] = 1
    else:
        current_id[entity_type] += 1
    
    return current_id[entity_type]