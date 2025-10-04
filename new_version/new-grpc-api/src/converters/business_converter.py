from src.public.tables import Business, BusinessSize
from domain.business import Business as DomainBusiness, BusinessSize as DomainBusinessSize

class BusinessConverter:
    
    SIZE_MAP = {
        1: DomainBusinessSize.SMALL,
        2: DomainBusinessSize.MEDIUM,
        3: DomainBusinessSize.LARGE
    }
    
    SIZE_REVERSE_MAP = {
        'SMALL': 1,
        'MEDIUM': 2,
        'LARGE': 3
    }
    
    @staticmethod
    def to_domain(db_business: Business) -> DomainBusiness:
        business_size = BusinessConverter.SIZE_MAP.get(
            db_business.business_size.code if db_business.business_size else 1,
            DomainBusinessSize.SMALL
        )
        
        return DomainBusiness(
            id=str(db_business.business_id),
            business_name=db_business.business_name,
            email=db_business.email,
            website_url=db_business.website_url or '',
            phone_number=db_business.phone_number or '',
            location_city=db_business.location_city or '',
            location_state=db_business.location_state or '',
            ein=db_business.ein or '',
            business_description=db_business.business_description or '',
            business_size=business_size
        )
    
    @staticmethod
    def size_to_code(size_str: str) -> int:
        return BusinessConverter.SIZE_REVERSE_MAP.get(size_str.upper(), 1)
    
    @staticmethod
    def size_to_string(size: DomainBusinessSize) -> str:
        return size.value
