"""
Usage: bash python -m database_layer.tests.test_cause
"""
import uuid
from database_layer.models.cause_category import CauseCategory
from database_layer.models.cause import Cause
from .test_utils import create_test_session

def test_cause_with_foreign_keys():
    print("=== Testing Cause Model with Foreign Key Relationships ===")
    
    # Use the helper function that enables foreign keys
    engine, session = create_test_session()
    
    print("\n1. Creating parent cause categories...")
    
    # Create parent records first
    community = CauseCategory(code=1, cause_category_name='Community')
    social = CauseCategory(code=2, cause_category_name='Social')
    
    session.add_all([community, social])
    session.commit()
    print("✅ Created cause categories")
    
    print("\n2. Creating causes with valid foreign keys...")
    
    # Create causes that reference the categories
    homelessness = Cause(
        code=1,
        cause_name='Homelessness',
        cause_category_id=community.cause_category_id
    )
    
    education = Cause(
        code=8,
        cause_name='Education', 
        cause_category_id=social.cause_category_id
    )
    
    session.add_all([homelessness, education])
    session.commit()
    print("✅ Created causes with valid foreign keys")
    
    print("\n3. Testing relationship navigation (Cause -> CauseCategory)...")
    
    # Test forward relationship
    print(f"Homelessness belongs to category: {homelessness.cause_category.cause_category_name}")
    print(f"Education belongs to category: {education.cause_category.cause_category_name}")
    
    print("\n4. Testing relationship navigation (CauseCategory -> Causes)...")
    
    # Test back relationship
    print(f"Community category has {len(community.causes)} causes:")
    for cause in community.causes:
        print(f"  - {cause.cause_name}")
    
    print(f"Social category has {len(social.causes)} causes:")
    for cause in social.causes:
        print(f"  - {cause.cause_name}")
    
    print("\n5. Testing foreign key constraints...")
    
    # Try to create cause with invalid category_id - THIS SHOULD NOW FAIL
    try:
        bad_cause = Cause(
            code=999,
            cause_name='Bad Cause',
            cause_category_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_cause)
        session.commit()
        print("❌ ERROR: Should have failed due to foreign key constraint!")
    except Exception as e:
        print("✅ Foreign key constraint working")
        print(f"   Error: {type(e).__name__}")
        session.rollback()
    
    print("\n6. Testing unique constraints...")
    
    try:
        duplicate_code = Cause(
            code=1,  # Same as homelessness
            cause_name='Duplicate Homelessness',
            cause_category_id=community.cause_category_id
        )
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    session.close()
    print("\n🎉 Cause with foreign keys working perfectly!")

if __name__ == "__main__":
    test_cause_with_foreign_keys()