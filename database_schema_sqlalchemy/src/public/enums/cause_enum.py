from enum import Enum

class CauseEnum(str, Enum):
    """
    Enum matching frontend cause codes and proto enum values.
    Must stay in sync with:
    - Frontend: mapCauseOptionToEnumValue.js
    - Proto: cause.proto CauseCode enum
    """
    
    # Community Causes
    HOMELESSNESS = "HOMELESSNESS"
    EVENTS_ADVOCACY = "EVENTS_ADVOCACY"
    FIRST_RESPONDERS = "FIRST_RESPONDERS"
    DISADVANTAGED_POPULATIONS = "DISADVANTAGED_POPULATIONS"
    SCHOOLS_TEACHERS = "SCHOOLS_TEACHERS"
    ANIMAL_WELFARE = "ANIMAL_WELFARE"
    
    # Social Causes
    SPORTS = "SPORTS"
    ARTS = "ARTS"
    FAITH_BASED_ORGS = "FAITH_BASED_ORGS"
    EDUCATION = "EDUCATION"
    SOCIAL_JUSTICE = "SOCIAL_JUSTICE"
    HEALTH_WELLBEING = "HEALTH_WELLBEING"
    
    # Innovation/Entrepreneurship
    YOUTH_EMPOWERMENT = "YOUTH_EMPOWERMENT"
    INNOVATION = "INNOVATION"
    SUSTAINABLE_INNOVATION = "SUSTAINABLE_INNOVATION"
    SOCIAL_ENTREPRENEURSHIP = "SOCIAL_ENTREPRENEURSHIP"
    
    # Environment
    DROUGHT_FIRE_MANAGEMENT = "DROUGHT_FIRE_MANAGEMENT"
    CLIMATE_ADVOCACY = "CLIMATE_ADVOCACY"
    WATER_SUSTAINABILITY = "WATER_SUSTAINABILITY"
    FOOD_SYSTEMS = "FOOD_SYSTEMS"
    WILDLIFE_PROTECTION = "WILDLIFE_PROTECTION"
    
    # Emergency
    EMERGENCY_RELIEF = "EMERGENCY_RELIEF"
    
    # Default/Error case
    UNSPECIFIED = "UNSPECIFIED"
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum, return UNSPECIFIED if not found"""
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.UNSPECIFIED
    
    @classmethod
    def get_display_name(cls, value):
        """Map enum value back to display name for frontend"""
        display_map = {
            cls.HOMELESSNESS: "Homelessness",
            cls.EVENTS_ADVOCACY: "Events & Advocacy",
            cls.FIRST_RESPONDERS: "First Responders",
            cls.DISADVANTAGED_POPULATIONS: "Disadvantaged Populations",
            cls.SCHOOLS_TEACHERS: "Schools & Teachers",
            cls.ANIMAL_WELFARE: "Animal Welfare",
            cls.SPORTS: "Sports",
            cls.ARTS: "Arts",
            cls.FAITH_BASED_ORGS: "Faith Based Orgs",
            cls.EDUCATION: "Education",
            cls.SOCIAL_JUSTICE: "Social Justice",
            cls.HEALTH_WELLBEING: "Health & Wellbeing",
            cls.YOUTH_EMPOWERMENT: "Youth Empowerment",
            cls.INNOVATION: "Innovation",
            cls.SUSTAINABLE_INNOVATION: "Sustainable Innovation",
            cls.SOCIAL_ENTREPRENEURSHIP: "Social Entrepreneurship",
            cls.DROUGHT_FIRE_MANAGEMENT: "Droughts & Fire Management",
            cls.CLIMATE_ADVOCACY: "Climate Advocacy",
            cls.WATER_SUSTAINABILITY: "Water Sustainability",
            cls.FOOD_SYSTEMS: "Food Systems",
            cls.WILDLIFE_PROTECTION: "Wildlife Protection",
            cls.EMERGENCY_RELIEF: "Emergency Relief",
        }
        return display_map.get(value, "Unknown")