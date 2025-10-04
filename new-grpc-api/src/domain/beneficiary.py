from enum import Enum

class BeneficiarySize(Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'

class Beneficiary:
    def __init__(self, id: str, beneficiary_name: str, email: str, **kwargs):
        self.id = id
        self.beneficiary_name = beneficiary_name
        self.email = email
        self.website_url = kwargs.get('website_url', '')
        self.phone_number = kwargs.get('phone_number', '')
        self.location_city = kwargs.get('location_city', '')
        self.location_state = kwargs.get('location_state', '')
        self.ein = kwargs.get('ein', '')
        self.beneficiary_description = kwargs.get('beneficiary_description', '')
        self.beneficiary_size = kwargs.get('beneficiary_size', BeneficiarySize.SMALL)
