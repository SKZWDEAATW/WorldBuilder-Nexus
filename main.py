import json
from storage import *
from models import World, Region
from ai_assistant import generate_ai_region

file = "data.json"

def get_world_names():
    """Lists out created world names"""
    data = load_worlds()
    for i, w in enumerate(data, 1): # This adds a nice number (1, 2, 3) next to each name
        print(f"{i}. {w.name}")

def get_world_region_names():
    data = load_worlds()
    data = [World.to_dict(w) for w in data]
    for w_idx, world in enumerate(data, 1):
        print(f"{w_idx}. {world['name']}")
        for r_idx, region in enumerate(world["regions"], 1):
            print(f"\t {r_idx}. {region['name']}: {region['description']}")



while True:
    print("\n--------------------------")
    print("1. Create a world")
    print("2. View worlds")
    print("3. Add region")
    print("4. Delete a world")
    print("5. Delete a region")
    print("6. Change world description")
    print("7. Change region description")
    print("8. Exit")
    print("9. AI generate region")
    act = input("What do you wish to do? ")
    match act:
        case "1":
            name = input("World name: ")
            genre = input("World genre: ")
            description = input("World description: ")
            regions = []

            world = World( #World instance
                name,
                genre, 
                description,
                regions
            )

            data = load_worlds() #returns a list of world objects
            data.append(world) #convert object into dict and add to list
            save_worlds(data)

            print(f"{name} has been created.")




        case "2":
            try:
                data = load_worlds()
                data = [World.to_dict(w) for w in data]
                for i, world in enumerate(data, 1): #world is a dictionary
                    print(f"{i}. {world['name']} (Genre: {world['genre']})")
                    print(f"Description: {world['description']}")
                    for i in range(0, len(world['regions'])):
                        print(f"\t{world['regions'][i]['name']}: {world['regions'][i]['description']}")
            except:
                print("No worlds have been created yet.")
                continue




        case "3": #add region
            data = load_worlds()
            get_world_names()
                
            try:
                select = int(input("What world do you wish to add a new region to? "))
                select-=1
                selected_world = data[select]
            except:
                print(f"Only {len(data)} worlds have been created")
                continue

            reg_name = input("Region name: ")
            reg_type = input("Region type: ")
            reg_description = input("Region description: ")
            reg_climate = input("Region climate: ")
            reg_rules = input("Region rules: ")

            region = Region(
                reg_name,
                reg_type,
                reg_description,
                reg_climate,
                reg_rules
            )
                                    
            selected_world.add_region(region)
            save_worlds(data)
            
            print(f"{reg_name} has been added to {selected_world.name}")



        case "4":
            get_world_names()
            try:
                selection = int(input("Which world do you wish to delete? "))
                # The backend handles the work and tells us if it worked!
                if delete_world(selection): 
                    print("World deleted successfully!")
                else:
                    print("Invalid world number.")
                    continue
            except ValueError:
                print("Please type a valid number.")
                continue

        
        case "5":
            data = load_worlds()
            get_world_region_names()
            try:
                ws = int(input("Which world contains the region you want to delete? "))
                rs = int(input("Which region do you wish to delete? "))
                if delete_region(ws, rs):
                    print("Region deleted successfully!")
                else:
                    print("Invalid number!")
            except:
                print("Check the world/region number!")
                continue


        case "6":
            get_world_names()
            try:
                selection = int(input("Which world do you wish to update? "))
                
                # Present the sub-menu options for the world attributes
                print("\nWhat attribute do you want to change?")
                print("1. Name")
                print("2. Genre")
                print("3. Description")
                attribute_choice = input("Enter choice (1-3): ")

                # Map the user's choice to the actual attribute names of your World class
                if attribute_choice == "1":
                    field_name = "name"
                elif attribute_choice == "2":
                    field_name = "genre"
                elif attribute_choice == "3":
                    field_name = "description"
                else:
                    print("Invalid attribute selection.")
                    continue

                new_value = input(f"Enter the new value for the world's {field_name}: ")

                if update_world_field(selection, field_name, new_value):
                    print(f"World {field_name} updated successfully!")
                else:
                    print("Invalid world number.")
            except ValueError:
                print("Please type a valid number.")
            continue


        case "7":
            get_world_region_names()
            try:
                ws = int(input("Which world contains the region you want to update? "))
                rs = int(input("Which region do you wish to change? "))
                
                # Sub-menu for region attributes
                print("\nWhat attribute do you want to change?")
                print("1. Name")
                print("2. Type")
                print("3. Description")
                print("4. Climate")
                print("5. Rules")
                attribute_choice = input("Enter choice (1-5): ")

                # Mapping choices to your Region class properties
                if attribute_choice == "1":
                    field_name = "name"
                elif attribute_choice == "2":
                    field_name = "type"
                elif attribute_choice == "3":
                    field_name = "description"
                elif attribute_choice == "4":
                    field_name = "climate"
                elif attribute_choice == "5":
                    field_name = "rules"
                else:
                    print("Invalid attribute selection.")
                    continue

                new_value = input(f"Enter the new value for the region's {field_name}: ")

                if update_region_field(ws, rs, field_name, new_value):
                    print(f"Region {field_name} updated successfully!")
                else:
                    print("Check the inserted numbers!")
            except ValueError:
                print("Please type valid numbers.")
            continue
            
        
        case "8":
            print("Goodbye, Traveler!")
            exit()

        case "9":
            get_world_names()
            try:
                selection = int(input(("Which world do you want to add an AI region to? ")))
                data = load_worlds()
                selected_world = data[selection-1]
            except:
                print("Invalid world choice!")
                continue

            theme = input("What theme or vibe should the AI generate? ")
            print("\nSynthesizing lore via AI... please wait.")
            ai_data = generate_ai_region(theme)

            new_region = Region(name=ai_data["name"],
                                type=ai_data["type"],
                                description=ai_data["description"],
                                climate=ai_data["climate"],
                                rules=ai_data["rules"])
            
            selected_world.regions.append(new_region)
            save_worlds(data)

            print(f"Success! AI generated the region: {new_region.name}")
            continue