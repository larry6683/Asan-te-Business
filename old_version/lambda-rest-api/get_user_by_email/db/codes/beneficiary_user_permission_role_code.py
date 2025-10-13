from enum import Enum
from typing import Self

class BeneficiaryUserPermissionRoleCode(Enum):
    ADMIN = 1
    TEAM_MEMBER = 2

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return BeneficiaryUserPermissionRoleCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return BeneficiaryUserPermissionRoleCode(value)
        except:
            return None