from enum import Enum

class RankEnum(str, Enum):
    """
    Enum for cause preference ranks.
    Must stay in sync with:
    - Frontend: mapRankToEnumValue.js
    - Proto: cause.proto CauseRank enum
    - Database: cause_preference_rank table
    """
    
    RANK_PRIMARY = "RANK_PRIMARY"
    RANK_SUPPORTING = "RANK_SUPPORTING"
    RANK_UNRANKED = "RANK_UNRANKED"
    RANK_UNSPECIFIED = "RANK_UNSPECIFIED"
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum, return RANK_UNSPECIFIED if not found"""
        # Handle both "PRIMARY" and "RANK_PRIMARY" formats
        if not value.startswith("RANK_"):
            value = f"RANK_{value}"
        
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.RANK_UNSPECIFIED
    
    @classmethod
    def to_db_name(cls, value):
        """Convert enum to database rank name (matches DB exactly now)"""
        db_map = {
            cls.RANK_PRIMARY: "PRIMARY",           # DB stores "PRIMARY"
            cls.RANK_SUPPORTING: "SUPPORTING",     # DB stores "SUPPORTING"
            cls.RANK_UNRANKED: "UNRANKED",         # DB stores "UNRANKED"
            cls.RANK_UNSPECIFIED: "UNSPECIFIED",   # DB stores "UNSPECIFIED"
        }
        return db_map.get(value, "UNSPECIFIED")
    
    @classmethod
    def from_db_name(cls, db_value: str):
        """Convert database name to enum"""
        # DB stores "PRIMARY", convert to "RANK_PRIMARY" enum
        return cls.from_string(db_value)