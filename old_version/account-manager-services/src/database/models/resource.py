from dataclasses import dataclass
from enum import IntEnum

class ResourceCategoryCode(IntEnum):
    HARDWARE = 1
    SOFTWARE = 2
    SERVICE = 3

@dataclass(slots=True)
class ResourceDbo:
    resource_id: str
    name: str
    description: str
    category: ResourceCategoryCode