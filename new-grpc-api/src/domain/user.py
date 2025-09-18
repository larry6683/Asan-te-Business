from enum import Enum
from dataclasses import dataclass

class UserType(Enum):
    BUSINESS = 1
    BENEFICIARY = 2
    CONSUMER = 3

@dataclass
class User:
    id: str
    email: str
    user_type: UserType

@dataclass  
class CreateUserData:
    email: str
    user_type: UserType
    mailing_list_signup: bool
