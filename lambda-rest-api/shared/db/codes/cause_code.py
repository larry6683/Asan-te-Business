from enum import Enum
from typing import Self

class CauseCode(Enum):
    # Community Causes
    HOMELESSNESS = 1
    EVENTS_ADVOCACY = 2
    FIRST_RESPONDERS = 3
    DISADVANTAGED_POPULATIONS = 4
    SCHOOLS_TEACHERS = 5

    # Social Causes
    SPORTS = 6
    ARTS = 7
    EDUCATION = 8
    SOCIAL_JUSTICE = 9
    MENTAL_HEALTH = 10

    # Innovation Causes
    YOUTH_EMPOWERMENT = 11
    SOCIAL_INNOVATION = 12
    SUSTAINABLE_INNOVATION = 13
    SOCIAL_ENTREPRENEURSHIP = 14

    # Environment
    DROUGHT_FIRE_MANAGEMENT = 15
    CLIMATE_ADVOCACY = 16
    CLIMATE_REFUGEES = 17
    WATER_SUSTAINABILITY = 18

    # Emergency Relief
    EMERGENCY_RELIEF = 19

    @staticmethod
    def from_str(value: str) -> Self:
        try:
            return CauseCode[value.upper()]
        except:
            return None

    @staticmethod
    def from_int(value: int) -> Self:
        try:
            return CauseCode(value)
        except:
            return None
