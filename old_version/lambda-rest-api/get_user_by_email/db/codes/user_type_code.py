from enum import Enum
from typing import Self

class UserTypeCode(Enum):
    BUSINESS = 1
    BENEFICIARY = 2
    CONSUMER = 3

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return UserTypeCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return UserTypeCode(value)
        except:
            None