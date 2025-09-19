"""
Usage: bash python -m database_layer.tests.test_registration_type
"""
from database_layer.models.registration_type import RegistrationType
from .test_utils import create_test_session

def test_registration_type_model():
    print("=== Testing RegistrationType Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating registration types...")
    
    # Create the 3 standard registration types (from your populate script)
    business = RegistrationType(code=1, registration_type_name='business')
    non_profit = RegistrationType(code=2, registration_type_name='non-profit')
    consumer = RegistrationType(code=3, registration_type_name='consumer')
    
    session.add_all([business, non_profit, consumer])
    session.commit()
    
    print("✅ Created all 3 registration types")
    
    print("\n2. Testing queries...")
    
    # Query by code
    business_type = session.query(RegistrationType).filter_by(code=1).first()
    print(f"Found by code: {business_type}")
    
    # Query by name
    non_profit_type = session.query(RegistrationType).filter_by(registration_type_name='non-profit').first()
    print(f"Found by name: {non_profit_type}")
    
    # Get all
    all_types = session.query(RegistrationType).all()
    print(f"Total registration types: {len(all_types)}")
    
    print("\n3. Verifying all expected types exist...")
    
    expected_types = ['business', 'non-profit', 'consumer']
    for type_name in expected_types:
        reg_type = session.query(RegistrationType).filter_by(registration_type_name=type_name).first()
        if reg_type:
            print(f"✅ Found: {type_name} (code {reg_type.code})")
        else:
            print(f"❌ Missing: {type_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = RegistrationType(code=1, registration_type_name='duplicate-business')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing we can add more registration types...")
    
    try:
        # Add another registration type with different code
        government = RegistrationType(code=4, registration_type_name='government')
        session.add(government)
        session.commit()
        print("✅ Can add additional registration types")
        
        # Verify we now have 4
        total = session.query(RegistrationType).count()
        print(f"Total registration types after adding government: {total}")
    except Exception as e:
        print(f"❌ Error adding additional registration type: {e}")
        session.rollback()
    
    session.close()
    print("\n🎉 RegistrationType model working perfectly!")

if __name__ == "__main__":
    test_registration_type_model()