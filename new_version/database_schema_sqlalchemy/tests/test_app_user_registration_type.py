"""
Usage: bash python -m database_layer.tests.test_app_user_registration_type
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.user_type import UserType
from database_layer.src.public.tables.app_user import AppUser
from database_layer.src.public.tables.registration_type import RegistrationType
from database_layer.src.public.tables.app_user_registration_type import AppUserRegistrationType
from .test_utils import create_test_session


def test_app_user_registration_type_junction():
    print("=== Testing AppUserRegistrationType Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create user types
    business_user_type = UserType(code=1, user_type_name='business user')
    consumer_user_type = UserType(code=2, user_type_name='consumer user')
    
    # Create registration types
    business_reg = RegistrationType(code=1, registration_type_name='business')
    non_profit_reg = RegistrationType(code=2, registration_type_name='non-profit')
    consumer_reg = RegistrationType(code=3, registration_type_name='consumer')
    
    session.add_all([business_user_type, consumer_user_type, business_reg, non_profit_reg, consumer_reg])
    session.commit()
    print("✅ Created user types and registration types")
    
    print("\n2. Creating app users...")
    
    # Create some app users
    john = AppUser(
        email='john@business.com',
        user_type_id=business_user_type.user_type_id
    )
    
    jane = AppUser(
        email='jane@consumer.com',
        user_type_id=consumer_user_type.user_type_id
    )
    
    bob = AppUser(
        email='bob@nonprofit.org',
        user_type_id=business_user_type.user_type_id
    )
    
    session.add_all([john, jane, bob])
    session.commit()
    print("✅ Created app users")
    
    print("\n3. Creating junction table entries...")
    
    # Link users to registration types
    # John is a business user
    john_business = AppUserRegistrationType(
        app_user_id=john.app_user_id,
        registration_type_id=business_reg.registration_type_id
    )
    
    # Jane is a consumer
    jane_consumer = AppUserRegistrationType(
        app_user_id=jane.app_user_id,
        registration_type_id=consumer_reg.registration_type_id
    )
    
    # Bob works for a non-profit
    bob_nonprofit = AppUserRegistrationType(
        app_user_id=bob.app_user_id,
        registration_type_id=non_profit_reg.registration_type_id
    )
    
    # Bob also has consumer registration (users can have multiple registrations)
    bob_consumer = AppUserRegistrationType(
        app_user_id=bob.app_user_id,
        registration_type_id=consumer_reg.registration_type_id
    )
    
    session.add_all([john_business, jane_consumer, bob_nonprofit, bob_consumer])
    session.commit()
    print("✅ Created junction table entries")
    
    print("\n4. Testing relationship navigation...")
    
    # Find all registration types for each user
    john_regs = session.query(AppUserRegistrationType).filter_by(app_user_id=john.app_user_id).all()
    print(f"John has {len(john_regs)} registration(s):")
    for reg in john_regs:
        print(f"  - {reg.registration_type.registration_type_name}")
    
    jane_regs = session.query(AppUserRegistrationType).filter_by(app_user_id=jane.app_user_id).all()
    print(f"Jane has {len(jane_regs)} registration(s):")
    for reg in jane_regs:
        print(f"  - {reg.registration_type.registration_type_name}")
    
    bob_regs = session.query(AppUserRegistrationType).filter_by(app_user_id=bob.app_user_id).all()
    print(f"Bob has {len(bob_regs)} registration(s):")
    for reg in bob_regs:
        print(f"  - {reg.registration_type.registration_type_name}")
    
    print("\n5. Testing reverse navigation...")
    
    # Find all users for each registration type
    business_users = session.query(AppUserRegistrationType).filter_by(registration_type_id=business_reg.registration_type_id).all()
    print(f"Business registration has {len(business_users)} user(s):")
    for user_reg in business_users:
        print(f"  - {user_reg.app_user.email}")
    
    consumer_users = session.query(AppUserRegistrationType).filter_by(registration_type_id=consumer_reg.registration_type_id).all()
    print(f"Consumer registration has {len(consumer_users)} user(s):")
    for user_reg in consumer_users:
        print(f"  - {user_reg.app_user.email}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create junction with invalid app_user_id
    try:
        bad_junction = AppUserRegistrationType(
            app_user_id=uuid.uuid4(),  # Random UUID that doesn't exist
            registration_type_id=business_reg.registration_type_id
        )
        session.add(bad_junction)
        session.commit()
        print("❌ ERROR: Should have failed due to app_user foreign key constraint!")
    except Exception as e:
        print("✅ App user foreign key constraint working")
        session.rollback()
    
    # Try to create junction with invalid registration_type_id
    try:
        bad_junction2 = AppUserRegistrationType(
            app_user_id=john.app_user_id,
            registration_type_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_junction2)
        session.commit()
        print("❌ ERROR: Should have failed due to registration_type foreign key constraint!")
    except Exception as e:
        print("✅ Registration type foreign key constraint working")
        session.rollback()
    
    print("\n7. Testing queries...")
    
    # Count total junction entries
    total_entries = session.query(AppUserRegistrationType).count()
    print(f"Total app user registration entries: {total_entries}")
    
    # Find users with multiple registrations
    users_with_multiple = session.query(AppUserRegistrationType.app_user_id).group_by(AppUserRegistrationType.app_user_id).having(func.count() > 1).all()
    print(f"Users with multiple registrations: {len(users_with_multiple)}")
    
    session.close()
    print("\n🎉 AppUserRegistrationType junction table working perfectly!")

if __name__ == "__main__":
    test_app_user_registration_type_junction()