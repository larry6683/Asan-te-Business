from enum import Enum

class BusinessSize(Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'

class Business:
    def __init__(self, id: str, business_name: str, email: str, **kwargs):
        self.id = id
        self.business_name = business_name
        self.email = email
        self.website_url = kwargs.get('website_url', '')
        self.phone_number = kwargs.get('phone_number', '')
        self.location_city = kwargs.get('location_city', '')
        self.location_state = kwargs.get('location_state', '')
        self.ein = kwargs.get('ein', '')
        self.business_description = kwargs.get('business_description', '')
        self.business_size = kwargs.get('business_size', BusinessSize.SMALL)
