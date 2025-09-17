from enum import Enum
from typing import Self

class SocialMediaTypeCode(Enum):
    UNSPECIFIED = 0
    LINKDIN = 1
    INSTAGRAM = 2
    FACEBOOK = 3

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return SocialMediaTypeCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return SocialMediaTypeCode(value)
        except:
            return None
        