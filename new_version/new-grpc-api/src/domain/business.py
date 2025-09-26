from enum import Enum

class BusinessSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM" 
    LARGE = "LARGE"

class Business:
    def __init__(self, id: str, business_name: str, email: str, website_url: str = None,
                 phone_number: str = None, location_city: str = None, location_state: str = None,
                 ein: str = None, business_description: str = "", business_size: BusinessSize = BusinessSize.SMALL):
        self.id = id
        self.business_name = business_name
        self.email = email
        self.website_url = website_url
        self.phone_number = phone_number
        self.location_city = location_city
        self.location_state = location_state
        self.ein = ein
        self.business_description = business_description
        self.business_size = business_size
