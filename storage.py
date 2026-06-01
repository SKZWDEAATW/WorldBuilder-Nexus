import json
from models import World

file = "data.json"

def load_worlds():
    try:
        with open(file, "r") as f:
            data = json.load(f) # data is a massive LIST of worlds from the JSON file
            return [World.to_obj(w) for w in data] # Each 'w' is a single dictionary representing ONE world.
    except:
        return []

def save_worlds(save):
    data = [w.to_dict() for w in save]
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def delete_world(selection):
    success = True
    data = load_worlds()
    try:
        data.pop(selection-1)
    except:
        success = False
    save_worlds(data)
    return success



def delete_region(ws, rs):
    success = True
    data = load_worlds()
    try:
        data[ws-1].regions.pop(rs-1)
    except:
        success = False
    save_worlds(data)
    return success


def update_world_field(selection, field_name, new_value):
    success = True
    data = load_worlds()
    try:
        selected_world = data[selection - 1]
        # Dynamically sets the specified attribute (like name, genre, or description)
        #If field_name is "genre", Python translates that line to selected_world.genre = new_value on the fly
        setattr(selected_world, field_name, new_value)
        save_worlds(data)
    except:
        success = False
    return success

def update_region_field(ws, rs, field_name, new_value):
    success = True
    data = load_worlds()
    try:
        selected_world = data[ws - 1]
        selected_region = selected_world.regions[rs - 1]
        # Dynamically sets the specified region attribute (like climate, rules, or description)
        setattr(selected_region, field_name, new_value)
        save_worlds(data)
    except:
        success = False
    return success