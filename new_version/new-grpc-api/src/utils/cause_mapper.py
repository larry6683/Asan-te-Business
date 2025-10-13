# new-grpc-api/src/utils/cause_mapper.py
"""
Utility for mapping between frontend enum values and database cause names.
Place this file at: new-grpc-api/src/utils/cause_mapper.py
"""

class CauseMapper:
    """Maps between enum values (from frontend) and database cause names"""
    
    # Mapping from enum value to database cause name
    ENUM_TO_DB = {
        # Community causes
        "HOMELESSNESS": "Homelessness",
        "EVENTS_ADVOCACY": "Events & Advocacy",
        "FIRST_RESPONDERS": "First Responders",
        "DISADVANTAGED_POPULATIONS": "Disadvantaged Populations",
        "SCHOOLS_TEACHERS": "Schools & Teachers",
        "ANIMAL_WELFARE": "Animal Welfare",
        
        # Social causes
        "SPORTS": "Sports",
        "ARTS": "Arts",
        "FAITH_BASED_ORGS": "Faith Based Orgs",
        "EDUCATION": "Education",
        "SOCIAL_JUSTICE": "Social Justice",
        "HEALTH_WELLBEING": "Health & Wellbeing",
        
        # Innovation/Entrepreneurship
        "YOUTH_EMPOWERMENT": "Youth Empowerment",
        "INNOVATION": "Innovation",
        "SUSTAINABLE_INNOVATION": "Sustainable Innovation",
        "SOCIAL_ENTREPRENEURSHIP": "Social Entrepreneurship",
        
        # Environment
        "DROUGHTS_FIRE_MANAGEMENT": "Droughts & Fire Management",
        "CLIMATE_ADVOCACY": "Climate Advocacy",
        "WATER_SUSTAINABILITY": "Water Sustainability",
        "FOOD_SYSTEMS": "Food Systems",
        "WILDLIFE_PROTECTION": "Wildlife Protection",
        
        # Emergency Relief
        "EMERGENCY_RELIEF": "Emergency Relief",
    }
    
    # Reverse mapping (if needed)
    DB_TO_ENUM = {v: k for k, v in ENUM_TO_DB.items()}
    
    @classmethod
    def enum_to_db_name(cls, enum_value: str) -> str:
        """
        Convert enum value to database cause name
        Returns the enum value unchanged if no mapping exists
        """
        return cls.ENUM_TO_DB.get(enum_value, enum_value)
    
    @classmethod
    def db_name_to_enum(cls, db_name: str) -> str:
        """
        Convert database cause name to enum value
        Returns the db_name unchanged if no mapping exists
        """
        return cls.DB_TO_ENUM.get(db_name, db_name)
    
    @classmethod
    def batch_enum_to_db(cls, enum_values: list) -> list:
        """Convert a list of enum values to database names"""
        return [cls.enum_to_db_name(val) for val in enum_values]
    
    @classmethod
    def batch_db_to_enum(cls, db_names: list) -> list:
        """Convert a list of database names to enum values"""
        return [cls.db_name_to_enum(name) for name in db_names]