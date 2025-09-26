from dataclasses import dataclass
from enum import Enum

class BusinessSizeCode(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    
    @staticmethod
    def from_str(value: str):
        try:
            return BusinessSizeCode[value.upper()]
        except:
            return BusinessSizeCode.SMALL

    @staticmethod
    def from_int(value: int):
        try:
            return BusinessSizeCode(value)
        except:
            return BusinessSizeCode.SMALL

@dataclass(slots=True)
class BusinessDbo:
    business_id: str
    business_name: str
    email: str
    website_url: str = None
    phone_number: str = None
    location_city: str = None
    location_state: str = None
    ein: str = None
    business_description: str = ""
    business_size_code: BusinessSizeCode = BusinessSizeCode.SMALL
