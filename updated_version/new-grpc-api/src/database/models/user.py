from dataclasses import dataclass
from enum import Enum

class UserTypeCode(Enum):
    BUSINESS = 1
    BENEFICIARY = 2
    CONSUMER = 3
    
    @staticmethod
    def from_str(value: str):
        try:
            return UserTypeCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int):
        try:
            return UserTypeCode(value)
        except:
            return None

@dataclass(slots=True)
class UserDbo:
    app_user_id: str
    email: str
    user_type_code: UserTypeCode
    mailing_list_signup: bool = False
