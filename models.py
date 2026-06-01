class World:
    def __init__(self, name, genre, description, regions=None):
        self.name = name
        self.genre = genre
        self.description = description
        self.regions = regions if regions is not None else []

    def to_dict(self):
            return{
                "name": self.name,
                "genre": self.genre,
                "description": self.description,
                "regions": [r.to_dict() for r in self.regions]
            }
            
    def add_region(self, region):
            self.regions.append(region)

    @classmethod
    def to_obj(cls, data): #turns json world data into a World object
        #FROM JSON TO PYTHON
        loaded_regions = [Region.to_obj(r) for r in data.get("regions", [])]
        return cls(
            data["name"],
            data["genre"],
            data["description"],
            loaded_regions #list of region pobjects
        )
            
    

class Region:
    def __init__(self, name, type, description, climate, rules, map_x=None, map_y=None, image_url=None):
        self.name = name
        self.type = type
        self.description = description
        self.climate = climate
        self.rules= rules
        self.map_x = map_x
        self.map_y = map_y
        self.image_url = image_url

    def to_dict(self):
            return{
                "name": self.name,
                "type": self.type,
                "description": self.description,
                "climate": self.climate,
                "rules": self.rules,
                "map_x": self.map_x,
                "map_y": self.map_y,
                "image_url":self.image_url
            }
    
    @classmethod
    def to_obj(cls, region):
        return cls(
            name=region["name"],
            type=region["type"],
            description=region["description"],
            climate=region["climate"],
            rules=region["rules"],
            map_x=region.get("map_x"), #prevents your script from crashing when reading old worlds in your data.json that don't have coordinates saved yet
            map_y=region.get("map_y"),
            image_url=region.get("image_url")
        )
                