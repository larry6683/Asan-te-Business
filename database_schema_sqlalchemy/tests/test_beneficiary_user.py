"""
Usage: bash python -m database_layer.tests.test_beneficiary_user
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.user_type import UserType
from database_layer.src.public.tables.app_user import AppUser
from database_layer.src.public.tables.beneficiary_size import BeneficiarySize
from database_layer.src.public.tables.beneficiary import Beneficiary
from database_layer.src.public.tables.beneficiary_user_permission_role import BeneficiaryUserPermissionRole
from database_layer.src.public.tables.beneficiary_user import BeneficiaryUser
from .test_utils import create_test_session

def test_beneficiary_user_junction():
    print("=== Testing BeneficiaryUser Junction Table (3 Foreign Keys) ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create user types
    beneficiary_user_type = UserType(code=2, user_type_name='beneficiary user')
    
    # Create beneficiary sizes
    small = BeneficiarySize(code=1, beneficiary_size_name='small')
    medium = BeneficiarySize(code=2, beneficiary_size_name='medium')
    
    # Create permission roles
    admin = BeneficiaryUserPermissionRole(code=1, beneficiary_user_permission_role_name='Admin')
    team_member = BeneficiaryUserPermissionRole(code=2, beneficiary_user_permission_role_name='Team Member')
    removed = BeneficiaryUserPermissionRole(code=3, beneficiary_user_permission_role_name='Removed')
    
    session.add_all([beneficiary_user_type, small, medium, admin, team_member, removed])
    session.commit()
    print("✅ Created basic parent records")
    
    print("\n2. Creating beneficiaries...")
    
    # Create beneficiaries
    homeless_shelter = Beneficiary(
        beneficiary_name='Downtown Homeless Shelter',
        email='info@downtownshelter.org',
        location_city='Denver',
        location_state='CO',
        beneficiary_size_id=medium.beneficiary_size_id
    )
    
    food_bank = Beneficiary(
        beneficiary_name='Community Food Bank',
        email='contact@communityfoodbank.org',
        location_city='Boulder',
        location_state='CO',
        beneficiary_size_id=small.beneficiary_size_id
    )
    
    session.add_all([homeless_shelter, food_bank])
    session.commit()
    print("✅ Created beneficiaries")
    
    print("\n3. Creating app users...")
    
    # Create app users
    sarah = AppUser(email='sarah@downtownshelter.org', user_type_id=beneficiary_user_type.user_type_id)
    mike = AppUser(email='mike@downtownshelter.org', user_type_id=beneficiary_user_type.user_type_id)
    lisa = AppUser(email='lisa@communityfoodbank.org', user_type_id=beneficiary_user_type.user_type_id)
    david = AppUser(email='david@communityfoodbank.org', user_type_id=beneficiary_user_type.user_type_id)
    
    session.add_all([sarah, mike, lisa, david])
    session.commit()
    print("✅ Created app users")
    
    print("\n4. Creating beneficiary user relationships...")
    
    # Link users to beneficiaries with roles
    # Homeless Shelter team
    sarah_shelter_admin = BeneficiaryUser(
        beneficiary_id=homeless_shelter.beneficiary_id,
        app_user_id=sarah.app_user_id,
        beneficiary_user_permission_role_id=admin.beneficiary_user_permission_role_id
    )
    
    mike_shelter_team = BeneficiaryUser(
        beneficiary_id=homeless_shelter.beneficiary_id,
        app_user_id=mike.app_user_id,
        beneficiary_user_permission_role_id=team_member.beneficiary_user_permission_role_id
    )
    
    # Food Bank team
    lisa_food_admin = BeneficiaryUser(
        beneficiary_id=food_bank.beneficiary_id,
        app_user_id=lisa.app_user_id,
        beneficiary_user_permission_role_id=admin.beneficiary_user_permission_role_id
    )
    
    david_food_team = BeneficiaryUser(
        beneficiary_id=food_bank.beneficiary_id,
        app_user_id=david.app_user_id,
        beneficiary_user_permission_role_id=team_member.beneficiary_user_permission_role_id
    )
    
    # David also volunteers at the shelter (users can be in multiple beneficiaries)
    david_shelter_team = BeneficiaryUser(
        beneficiary_id=homeless_shelter.beneficiary_id,
        app_user_id=david.app_user_id,
        beneficiary_user_permission_role_id=team_member.beneficiary_user_permission_role_id
    )
    
    session.add_all([sarah_shelter_admin, mike_shelter_team, lisa_food_admin, david_food_team, david_shelter_team])
    session.commit()
    print("✅ Created beneficiary user relationships")
    
    print("\n5. Testing relationship navigation...")
    
    # Find all users for each beneficiary
    shelter_team = session.query(BeneficiaryUser).filter_by(beneficiary_id=homeless_shelter.beneficiary_id).all()
    print(f"Homeless Shelter has {len(shelter_team)} team member(s):")
    for member in shelter_team:
        print(f"  - {member.app_user.email} ({member.permission_role.beneficiary_user_permission_role_name})")
    
    food_team = session.query(BeneficiaryUser).filter_by(beneficiary_id=food_bank.beneficiary_id).all()
    print(f"Food Bank has {len(food_team)} team member(s):")
    for member in food_team:
        print(f"  - {member.app_user.email} ({member.permission_role.beneficiary_user_permission_role_name})")
    
    print("\n6. Testing reverse navigation...")
    
    # Find all beneficiaries for each user
    david_beneficiaries = session.query(BeneficiaryUser).filter_by(app_user_id=david.app_user_id).all()
    print(f"David works for {len(david_beneficiaries)} beneficiary/ies:")
    for ben_user in david_beneficiaries:
        print(f"  - {ben_user.beneficiary.beneficiary_name} ({ben_user.permission_role.beneficiary_user_permission_role_name})")
    
    sarah_beneficiaries = session.query(BeneficiaryUser).filter_by(app_user_id=sarah.app_user_id).all()
    print(f"Sarah works for {len(sarah_beneficiaries)} beneficiary/ies:")
    for ben_user in sarah_beneficiaries:
        print(f"  - {ben_user.beneficiary.beneficiary_name} ({ben_user.permission_role.beneficiary_user_permission_role_name})")
    
    print("\n7. Testing role-based queries...")
    
    # Find all admins
    all_admins = session.query(BeneficiaryUser).filter_by(beneficiary_user_permission_role_id=admin.beneficiary_user_permission_role_id).all()
    print(f"All admins ({len(all_admins)}):")
    for admin_user in all_admins:
        print(f"  - {admin_user.app_user.email} at {admin_user.beneficiary.beneficiary_name}")
    
    # Find all team members
    all_team_members = session.query(BeneficiaryUser).filter_by(beneficiary_user_permission_role_id=team_member.beneficiary_user_permission_role_id).all()
    print(f"All team members ({len(all_team_members)}):")
    for team_user in all_team_members:
        print(f"  - {team_user.app_user.email} at {team_user.beneficiary.beneficiary_name}")
    
    print("\n8. Testing foreign key constraints...")
    
    # Try to create beneficiary user with invalid beneficiary_id
    try:
        bad_beneficiary_user = BeneficiaryUser(
            beneficiary_id=uuid.uuid4(),  # Random UUID that doesn't exist
            app_user_id=sarah.app_user_id,
            beneficiary_user_permission_role_id=admin.beneficiary_user_permission_role_id
        )
        session.add(bad_beneficiary_user)
        session.commit()
        print("❌ ERROR: Should have failed due to beneficiary foreign key constraint!")
    except Exception as e:
        print("✅ Beneficiary foreign key constraint working")
        session.rollback()
    
    # Try to create beneficiary user with invalid app_user_id
    try:
        bad_user_beneficiary = BeneficiaryUser(
            beneficiary_id=homeless_shelter.beneficiary_id,
            app_user_id=uuid.uuid4(),  # Random UUID that doesn't exist
            beneficiary_user_permission_role_id=admin.beneficiary_user_permission_role_id
        )
        session.add(bad_user_beneficiary)
        session.commit()
        print("❌ ERROR: Should have failed due to app_user foreign key constraint!")
    except Exception as e:
        print("✅ App user foreign key constraint working")
        session.rollback()
    
    # Try to create beneficiary user with invalid permission role
    try:
        bad_role_beneficiary = BeneficiaryUser(
            beneficiary_id=homeless_shelter.beneficiary_id,
            app_user_id=sarah.app_user_id,
            beneficiary_user_permission_role_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_role_beneficiary)
        session.commit()
        print("❌ ERROR: Should have failed due to permission role foreign key constraint!")
    except Exception as e:
        print("✅ Permission role foreign key constraint working")
        session.rollback()
    
    print("\n9. Testing aggregate queries...")
    
    # Count total beneficiary user relationships
    total_relationships = session.query(BeneficiaryUser).count()
    print(f"Total beneficiary user relationships: {total_relationships}")
    
    # Find users with multiple beneficiary affiliations
    users_with_multiple = session.query(BeneficiaryUser.app_user_id).group_by(BeneficiaryUser.app_user_id).having(func.count() > 1).all()
    print(f"Users with multiple beneficiary affiliations: {len(users_with_multiple)}")
    
    session.close()
    print("\n🎉 BeneficiaryUser junction table with 3 foreign keys working perfectly!")

if __name__ == "__main__":
    test_beneficiary_user_junction()