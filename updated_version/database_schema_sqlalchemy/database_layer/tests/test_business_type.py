"""
Usage: bash python -m database_layer.tests.test_business_type
"""
from database_layer.models.business_type import BusinessType
from .test_utils import create_test_session

def test_business_type_creation():
    """Test creating a business type"""
    engine, session = create_test_session()
    
    # Create business type
    business_type = BusinessType(
        business_type_name="business",
        code=1
    )
    
    session.add(business_type)
    session.commit()
    
    # Verify creation
    saved_type = session.query(BusinessType).filter_by(code=1).first()
    assert saved_type is not None
    assert saved_type.business_type_name == "business"
    assert saved_type.code == 1
    assert saved_type.business_type_id is not None
    
    session.close()
    print("✅ BusinessType creation test passed")

if __name__ == "__main__":
    test_business_type_creation()
    print("✅ All BusinessType tests passed!")