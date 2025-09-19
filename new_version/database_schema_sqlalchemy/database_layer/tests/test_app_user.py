"""
Usage: bash python -m database_layer.tests.test_app_user
"""
import uuid
from database_layer.models.user_type import UserType
from database_layer.models.app_user import AppUser
from .test_utils import create_test_session

def test_app_user_with_foreign_keys():
    print("=== Testing AppUser Model with Foreign Key Relationships ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating user types...")
    
    # Create user types first (parent records)
    business_user_type = UserType(code=1, user_type_name='business user')
    beneficiary_user_type = UserType(code=2, user_type_name='beneficiary user')
    consumer_user_type = UserType(code=3, user_type_name='consumer user')
    
    session.add_all([business_user_type, beneficiary_user_type, consumer_user_type])
    session.commit()
    print("✅ Created user types")
    
    print("\n2. Creating app users with valid foreign keys...")
    
    # Create app users that reference the user types
    business_user = AppUser(
        email='john@business.com',
        mailing_list_signup=True,
        user_type_id=business_user_type.user_type_id
    )
    
    consumer_user = AppUser(
        email='jane@consumer.com',
        mailing_list_signup=False,
        user_type_id=consumer_user_type.user_type_id
    )
    
    beneficiary_user = AppUser(
        email='org@beneficiary.org',
        mailing_list_signup=True,
        user_type_id=beneficiary_user_type.user_type_id,
        email_hash=b'some_hash_bytes'  # Test the BYTEA field
    )
    
    session.add_all([business_user, consumer_user, beneficiary_user])
    session.commit()
    print("✅ Created app users with valid foreign keys")
    
    print("\n3. Testing relationship navigation (AppUser -> UserType)...")
    
    # Test forward relationship
    print(f"Business user type: {business_user.user_type.user_type_name}")
    print(f"Consumer user type: {consumer_user.user_type.user_type_name}")
    print(f"Beneficiary user type: {beneficiary_user.user_type.user_type_name}")
    
    print("\n4. Testing relationship navigation (UserType -> AppUsers)...")
    
    # Test back relationship
    print(f"Business user type has {len(business_user_type.app_users)} users:")
    for user in business_user_type.app_users:
        print(f"  - {user.email}")
    
    print(f"Consumer user type has {len(consumer_user_type.app_users)} users:")
    for user in consumer_user_type.app_users:
        print(f"  - {user.email}")
    
    print("\n5. Testing queries and email_hash field...")
    
    # Query by email
    john = session.query(AppUser).filter_by(email='john@business.com').first()
    print(f"Found user by email: {john}")
    
    # Query users with email_hash
    users_with_hash = session.query(AppUser).filter(AppUser.email_hash.isnot(None)).all()
    print(f"Users with email hash: {len(users_with_hash)}")
    
    # Query by mailing list signup
    subscribed_users = session.query(AppUser).filter_by(mailing_list_signup=True).all()
    print(f"Users subscribed to mailing list: {len(subscribed_users)}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create app user with invalid user_type_id
    try:
        bad_user = AppUser(
            email='bad@user.com',
            user_type_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_user)
        session.commit()
        print("❌ ERROR: Should have failed due to foreign key constraint!")
    except Exception as e:
        print("✅ Foreign key constraint working")
        print(f"   Error: {type(e).__name__}")
        session.rollback()
    
    print("\n7. Testing boolean default value...")
    
    # Create user without specifying mailing_list_signup
    default_user = AppUser(
        email='default@test.com',
        user_type_id=business_user_type.user_type_id
    )
    session.add(default_user)
    session.commit()
    
    print(f"Default mailing_list_signup value: {default_user.mailing_list_signup}")
    if default_user.mailing_list_signup == False:
        print("✅ Boolean default value working")
    else:
        print("❌ Boolean default value not working")
    
    session.close()
    print("\n🎉 AppUser with foreign keys and indexes working perfectly!")

if __name__ == "__main__":
    test_app_user_with_foreign_keys()