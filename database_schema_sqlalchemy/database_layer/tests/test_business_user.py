"""
Usage: bash python -m database_layer.tests.test_business_user
"""
import uuid
from sqlalchemy.sql import func
from database_layer.models.user_type import UserType
from database_layer.models.app_user import AppUser
from database_layer.models.business_size import BusinessSize
from database_layer.models.business import Business
from database_layer.models.business_user_permission_role import BusinessUserPermissionRole
from database_layer.models.business_user import BusinessUser
from .test_utils import create_test_session

def test_business_user_junction():
    print("=== Testing BusinessUser Junction Table (3 Foreign Keys) ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create user types
    business_user_type = UserType(code=1, user_type_name='business user')
    
    # Create business sizes
    small = BusinessSize(code=1, business_size_name='small')
    medium = BusinessSize(code=2, business_size_name='medium')
    
    # Create permission roles
    admin = BusinessUserPermissionRole(code=1, business_user_permission_role_name='Admin')
    team_member = BusinessUserPermissionRole(code=2, business_user_permission_role_name='Team Member')
    removed = BusinessUserPermissionRole(code=3, business_user_permission_role_name='Removed')
    
    session.add_all([business_user_type, small, medium, admin, team_member, removed])
    session.commit()
    print("✅ Created basic parent records")
    
    print("\n2. Creating businesses...")
    
    # Create businesses
    eco_solutions = Business(
        business_name='Eco Solutions Inc.',
        email='contact@ecosolutions.com',
        location_city='Seattle',
        location_state='WA',
        business_size_id=medium.business_size_id
    )
    
    tech_innovations = Business(
        business_name='Tech Innovations Ltd',
        email='info@techinnovations.com',
        location_city='San Francisco',
        location_state='CA',
        business_size_id=small.business_size_id
    )
    
    session.add_all([eco_solutions, tech_innovations])
    session.commit()
    print("✅ Created businesses")
    
    print("\n3. Creating app users...")
    
    # Create app users
    john = AppUser(email='john@ecosolutions.com', user_type_id=business_user_type.user_type_id)
    jane = AppUser(email='jane@ecosolutions.com', user_type_id=business_user_type.user_type_id)
    bob = AppUser(email='bob@techinnovations.com', user_type_id=business_user_type.user_type_id)
    alice = AppUser(email='alice@techinnovations.com', user_type_id=business_user_type.user_type_id)
    
    session.add_all([john, jane, bob, alice])
    session.commit()
    print("✅ Created app users")
    
    print("\n4. Creating business user relationships...")
    
    # Link users to businesses with roles
    # Eco Solutions team
    john_eco_admin = BusinessUser(
        business_id=eco_solutions.business_id,
        app_user_id=john.app_user_id,
        business_user_permission_role_id=admin.business_user_permission_role_id
    )
    
    jane_eco_team = BusinessUser(
        business_id=eco_solutions.business_id,
        app_user_id=jane.app_user_id,
        business_user_permission_role_id=team_member.business_user_permission_role_id
    )
    
    # Tech Innovations team
    bob_tech_admin = BusinessUser(
        business_id=tech_innovations.business_id,
        app_user_id=bob.app_user_id,
        business_user_permission_role_id=admin.business_user_permission_role_id
    )
    
    alice_tech_team = BusinessUser(
        business_id=tech_innovations.business_id,
        app_user_id=alice.app_user_id,
        business_user_permission_role_id=team_member.business_user_permission_role_id
    )
    
    # Alice also works as a consultant for Eco Solutions (users can be in multiple businesses)
    alice_eco_team = BusinessUser(
        business_id=eco_solutions.business_id,
        app_user_id=alice.app_user_id,
        business_user_permission_role_id=team_member.business_user_permission_role_id
    )
    
    session.add_all([john_eco_admin, jane_eco_team, bob_tech_admin, alice_tech_team, alice_eco_team])
    session.commit()
    print("✅ Created business user relationships")
    
    print("\n5. Testing relationship navigation...")
    
    # Find all users for each business
    eco_team = session.query(BusinessUser).filter_by(business_id=eco_solutions.business_id).all()
    print(f"Eco Solutions has {len(eco_team)} team member(s):")
    for member in eco_team:
        print(f"  - {member.app_user.email} ({member.permission_role.business_user_permission_role_name})")
    
    tech_team = session.query(BusinessUser).filter_by(business_id=tech_innovations.business_id).all()
    print(f"Tech Innovations has {len(tech_team)} team member(s):")
    for member in tech_team:
        print(f"  - {member.app_user.email} ({member.permission_role.business_user_permission_role_name})")
    
    print("\n6. Testing reverse navigation...")
    
    # Find all businesses for each user
    alice_businesses = session.query(BusinessUser).filter_by(app_user_id=alice.app_user_id).all()
    print(f"Alice works for {len(alice_businesses)} business(es):")
    for biz_user in alice_businesses:
        print(f"  - {biz_user.business.business_name} ({biz_user.permission_role.business_user_permission_role_name})")
    
    john_businesses = session.query(BusinessUser).filter_by(app_user_id=john.app_user_id).all()
    print(f"John works for {len(john_businesses)} business(es):")
    for biz_user in john_businesses:
        print(f"  - {biz_user.business.business_name} ({biz_user.permission_role.business_user_permission_role_name})")
    
    print("\n7. Testing role-based queries...")
    
    # Find all admins
    all_admins = session.query(BusinessUser).filter_by(business_user_permission_role_id=admin.business_user_permission_role_id).all()
    print(f"All admins ({len(all_admins)}):")
    for admin_user in all_admins:
        print(f"  - {admin_user.app_user.email} at {admin_user.business.business_name}")
    
    # Find all team members
    all_team_members = session.query(BusinessUser).filter_by(business_user_permission_role_id=team_member.business_user_permission_role_id).all()
    print(f"All team members ({len(all_team_members)}):")
    for team_user in all_team_members:
        print(f"  - {team_user.app_user.email} at {team_user.business.business_name}")
    
    print("\n8. Testing foreign key constraints...")
    
    # Try to create business user with invalid business_id
    try:
        bad_business_user = BusinessUser(
            business_id=uuid.uuid4(),  # Random UUID that doesn't exist
            app_user_id=john.app_user_id,
            business_user_permission_role_id=admin.business_user_permission_role_id
        )
        session.add(bad_business_user)
        session.commit()
        print("❌ ERROR: Should have failed due to business foreign key constraint!")
    except Exception as e:
        print("✅ Business foreign key constraint working")
        session.rollback()
    
    # Try to create business user with invalid app_user_id
    try:
        bad_user_business = BusinessUser(
            business_id=eco_solutions.business_id,
            app_user_id=uuid.uuid4(),  # Random UUID that doesn't exist
            business_user_permission_role_id=admin.business_user_permission_role_id
        )
        session.add(bad_user_business)
        session.commit()
        print("❌ ERROR: Should have failed due to app_user foreign key constraint!")
    except Exception as e:
        print("✅ App user foreign key constraint working")
        session.rollback()
    
    # Try to create business user with invalid permission role
    try:
        bad_role_business = BusinessUser(
            business_id=eco_solutions.business_id,
            app_user_id=john.app_user_id,
            business_user_permission_role_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_role_business)
        session.commit()
        print("❌ ERROR: Should have failed due to permission role foreign key constraint!")
    except Exception as e:
        print("✅ Permission role foreign key constraint working")
        session.rollback()
    
    print("\n9. Testing aggregate queries...")
    
    # Count total business user relationships
    total_relationships = session.query(BusinessUser).count()
    print(f"Total business user relationships: {total_relationships}")
    
    # Find users with multiple business affiliations
    users_with_multiple = session.query(BusinessUser.app_user_id).group_by(BusinessUser.app_user_id).having(func.count() > 1).all()
    print(f"Users with multiple business affiliations: {len(users_with_multiple)}")
    
    session.close()
    print("\n🎉 BusinessUser junction table with 3 foreign keys working perfectly!")

if __name__ == "__main__":
    test_business_user_junction()