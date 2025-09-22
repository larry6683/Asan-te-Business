from enum import Enum
from typing import Self

class CausePreferenceRankCode(Enum):
    UNRANKED = 0
    PRIMARY = 1
    SUPPORTING = 2

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return CausePreferenceRankCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return CausePreferenceRankCode(value)
        except:
            return None