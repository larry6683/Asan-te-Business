from enum import Enum
from typing import Self

class BeneficiarySizeCode(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return BeneficiarySizeCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return BeneficiarySizeCode(value)
        except:
            return None