from enum import Enum
from typing import Self

class BusinessUserPermissionRoleCode(Enum):
    ADMIN = 1
    TEAM_MEMBER = 2

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return BusinessUserPermissionRoleCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return BusinessUserPermissionRoleCode(value)
        except:
            return None