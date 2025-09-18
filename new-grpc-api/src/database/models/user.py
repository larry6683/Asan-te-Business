from dataclasses import dataclass
from enum import Enum

class UserTypeCode(Enum):
    BUSINESS = 1
    BENEFICIARY = 2
    CONSUMER = 3

@dataclass(slots=True)
class UserDbo:
    app_user_id: str
    email: str
    user_type_code: UserTypeCode

@dataclass(slots=True)
class CreateUserDbo:
    email: str
    user_type_code: UserTypeCode
    mailing_list_signup: bool
