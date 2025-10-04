"""
Usage: bash python -m database_layer.tests.test_beneficiary_type
"""
from database_layer.src.public.tables.beneficiary_type import BeneficiaryType
from .test_utils import create_test_session

def test_beneficiary_type_creation():
    """Test creating a beneficiary type"""
    engine, session = create_test_session()
    
    # Create beneficiary type
    beneficiary_type = BeneficiaryType(
        beneficiary_type_name="non-profit",
        code=1
    )
    
    session.add(beneficiary_type)
    session.commit()
    
    # Verify creation
    saved_type = session.query(BeneficiaryType).filter_by(code=1).first()
    assert saved_type is not None
    assert saved_type.beneficiary_type_name == "non-profit"
    assert saved_type.code == 1
    assert saved_type.beneficiary_type_id is not None
    
    session.close()
    print("✅ BeneficiaryType creation test passed")

if __name__ == "__main__":
    test_beneficiary_type_creation()
    print("✅ All BeneficiaryType tests passed!")