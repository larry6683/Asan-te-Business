# new_version/new-grpc-api/src/converters/business_converter.py
import sys
import os

# Import path fix
sys.path.insert(0, os.path.dirname(__file__))
from database_path_fix import import_sqlalchemy_models

# Try to import SQLAlchemy models
Business, BusinessSize, SQLALCHEMY_AVAILABLE = import_sqlalchemy_models(['Business', 'BusinessSize'])

from domain.business import Business as DomainBusiness, BusinessSize as DomainBusinessSize

class BusinessConverter:
    @staticmethod
    def to_domain(business) -> DomainBusiness:
        """Convert SQLAlchemy Business to domain object"""
        if not SQLALCHEMY_AVAILABLE:
            raise ImportError("SQLAlchemy models not available")
            
        # Map business size codes to domain BusinessSize enum
        business_size_map = {
            1: DomainBusinessSize.SMALL,
            2: DomainBusinessSize.MEDIUM,
            3: DomainBusinessSize.LARGE
        }
        
        # Get business size code from the relationship
        business_size_code = business.business_size.code if business.business_size else 1
        domain_business_size = business_size_map.get(business_size_code, DomainBusinessSize.SMALL)
        
        return DomainBusiness(
            id=str(business.business_id),
            business_name=business.business_name,
            email=business.email,
            website_url=business.website_url,
            phone_number=business.phone_number,
            location_city=business.location_city,
            location_state=business.location_state,
            ein=business.ein,
            business_description=business.business_description or "",
            business_size=domain_business_size
        )
    
    @staticmethod
    def business_size_to_string(business_size: DomainBusinessSize) -> str:
        """Convert BusinessSize enum to string"""
        size_map = {
            DomainBusinessSize.SMALL: "SMALL",
            DomainBusinessSize.MEDIUM: "MEDIUM", 
            DomainBusinessSize.LARGE: "LARGE"
        }
        return size_map.get(business_size, "SMALL")
        
    @staticmethod
    def business_size_from_string(business_size_str: str) -> DomainBusinessSize:
        """Convert string to BusinessSize enum"""
        if not business_size_str:
            return DomainBusinessSize.SMALL
            
        business_size_map = {
            'SMALL': DomainBusinessSize.SMALL,
            'MEDIUM': DomainBusinessSize.MEDIUM,
            'LARGE': DomainBusinessSize.LARGE
        }
        return business_size_map.get(business_size_str.upper(), DomainBusinessSize.SMALL)
    
    @staticmethod
    def business_size_string_to_code(business_size_str: str) -> int:
        """Convert business size string to database code"""
        size_map = {
            'SMALL': 1,
            'MEDIUM': 2,
            'LARGE': 3
        }
        return size_map.get(business_size_str.upper(), 1)
