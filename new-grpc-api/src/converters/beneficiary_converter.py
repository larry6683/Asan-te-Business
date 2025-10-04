from src.public.tables import Beneficiary, BeneficiarySize
from domain.beneficiary import Beneficiary as DomainBeneficiary, BeneficiarySize as DomainBeneficiarySize

class BeneficiaryConverter:
    
    SIZE_MAP = {
        1: DomainBeneficiarySize.SMALL,
        2: DomainBeneficiarySize.MEDIUM,
        3: DomainBeneficiarySize.LARGE
    }
    
    SIZE_REVERSE_MAP = {
        'SMALL': 1,
        'MEDIUM': 2,
        'LARGE': 3
    }
    
    @staticmethod
    def to_domain(db_beneficiary: Beneficiary) -> DomainBeneficiary:
        beneficiary_size = BeneficiaryConverter.SIZE_MAP.get(
            db_beneficiary.beneficiary_size.code if db_beneficiary.beneficiary_size else 1,
            DomainBeneficiarySize.SMALL
        )
        
        return DomainBeneficiary(
            id=str(db_beneficiary.beneficiary_id),
            beneficiary_name=db_beneficiary.beneficiary_name,
            email=db_beneficiary.email,
            website_url=db_beneficiary.website_url or '',
            phone_number=db_beneficiary.phone_number or '',
            location_city=db_beneficiary.location_city or '',
            location_state=db_beneficiary.location_state or '',
            ein=db_beneficiary.ein or '',
            beneficiary_description=db_beneficiary.beneficiary_description or '',
            beneficiary_size=beneficiary_size
        )
    
    @staticmethod
    def size_to_code(size_str: str) -> int:
        return BeneficiaryConverter.SIZE_REVERSE_MAP.get(size_str.upper(), 1)
    
    @staticmethod
    def size_to_string(size: DomainBeneficiarySize) -> str:
        return size.value
