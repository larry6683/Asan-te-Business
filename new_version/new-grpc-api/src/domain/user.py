from enum import Enum

class UserType(Enum):
    BUSINESS = 'BUSINESS'
    BENEFICIARY = 'BENEFICIARY'
    CONSUMER = 'CONSUMER'

class User:
    def __init__(self, id: str, email: str, user_type: UserType, mailing_list_signup: bool = False):
        self.id = id
        self.email = email
        self.user_type = user_type
        self.mailing_list_signup = mailing_list_signup
