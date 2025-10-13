from enum import Enum
from typing import Self

class ShopTypeCode(Enum):
    SHOPIFY = 1

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return ShopTypeCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return ShopTypeCode(value)
        except:
            None