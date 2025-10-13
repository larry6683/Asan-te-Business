from utils import Utils

class ApiResource:
    def __init__(self, 
                type: str, 
                id: str, 
                attributes: dict, 
                links: dict = None,
                relationships: dict = None
                ):
        self.type = type
        self.id = id
        self.attributes = attributes
        self.relationships = relationships
        self.links = links

    # implemented to prevent null relationships & links from cropping up
    def to_dict(self):
        resource_dict = {}
        resource_dict["type"] = self.type
        resource_dict["id"] = self.id
        resource_dict["attributes"] = self.attributes
        if self.links is not None: resource_dict['links'] = self.links
        if self.relationships is not None: resource_dict["relationships"] = self.relationships
        return Utils.obj_to_dict(resource_dict)