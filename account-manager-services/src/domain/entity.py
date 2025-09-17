from enum import Enum

class EntityType(Enum):
    BUSINESS = 1
    BENEFICIARY = 2
    CONSUMER = 3

class Entity:
    def __init__(self, type: EntityType, id: str):
        self.entity_type = type
        self.id = id