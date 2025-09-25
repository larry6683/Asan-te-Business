# new_version/new-grpc-api/src/converters/user_converter.py
import sys
import os

# Import path fix
sys.path.insert(0, os.path.dirname(__file__))
from database_path_fix import import_sqlalchemy_models

# Try to import SQLAlchemy models
AppUser, UserType, SQLALCHEMY_AVAILABLE = import_sqlalchemy_models()

from domain.user import User, UserType as DomainUserType

class UserConverter:
    @staticmethod
    def to_domain(app_user) -> User:
        """Convert SQLAlchemy AppUser to domain object"""
        if not SQLALCHEMY_AVAILABLE:
            raise ImportError("SQLAlchemy models not available")
            
        # Map user type codes to domain UserType enum
        user_type_map = {
            1: DomainUserType.BUSINESS,    # business user
            2: DomainUserType.BENEFICIARY, # beneficiary user
            3: DomainUserType.CONSUMER     # consumer user
        }
        
        # Get user type code from the relationship
        user_type_code = app_user.user_type.code
        domain_user_type = user_type_map.get(user_type_code, DomainUserType.CONSUMER)
        
        return User(
            id=str(app_user.app_user_id),
            email=app_user.email,
            user_type=domain_user_type,
            mailing_list_signup=app_user.mailing_list_signup
        )
    
    @staticmethod
    def user_type_to_string(user_type: DomainUserType) -> str:
        """Convert UserType enum to string"""
        type_map = {
            DomainUserType.BUSINESS: "BUSINESS",
            DomainUserType.BENEFICIARY: "BENEFICIARY", 
            DomainUserType.CONSUMER: "CONSUMER"
        }
        return type_map.get(user_type, "CONSUMER")
        
    @staticmethod
    def user_type_from_string(user_type_str: str) -> DomainUserType:
        """Convert string to UserType enum"""
        if not user_type_str:
            return None
            
        user_type_map = {
            'BUSINESS': DomainUserType.BUSINESS,
            'BENEFICIARY': DomainUserType.BENEFICIARY,
            'CONSUMER': DomainUserType.CONSUMER
        }
        return user_type_map.get(user_type_str.upper())
    
    @staticmethod
    def user_type_string_to_code(user_type_str: str) -> int:
        """Convert user type string to database code"""
        type_map = {
            'BUSINESS': 1,
            'BENEFICIARY': 2,
            'CONSUMER': 3
        }
        return type_map.get(user_type_str.upper(), 1)