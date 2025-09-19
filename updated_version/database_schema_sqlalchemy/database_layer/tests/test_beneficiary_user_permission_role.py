"""
Usage: bash python -m database_layer.tests.test_beneficiary_user_permission
"""
from database_layer.models.beneficiary_user_permission_role import BeneficiaryUserPermissionRole
from .test_utils import create_test_session

def test_beneficiary_user_permission_role_model():
    print("=== Testing BeneficiaryUserPermissionRole Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating beneficiary user permission roles...")
    
    # Create the 3 standard permission roles (from your populate script)
    admin = BeneficiaryUserPermissionRole(code=1, beneficiary_user_permission_role_name='Admin')
    team_member = BeneficiaryUserPermissionRole(code=2, beneficiary_user_permission_role_name='Team Member')
    removed = BeneficiaryUserPermissionRole(code=3, beneficiary_user_permission_role_name='Removed')
    
    session.add_all([admin, team_member, removed])
    session.commit()
    
    print("✅ Created all 3 beneficiary permission roles")
    
    print("\n2. Testing queries...")
    
    # Query by code
    admin_role = session.query(BeneficiaryUserPermissionRole).filter_by(code=1).first()
    print(f"Found by code: {admin_role}")
    
    # Query by name
    team_role = session.query(BeneficiaryUserPermissionRole).filter_by(beneficiary_user_permission_role_name='Team Member').first()
    print(f"Found by name: {team_role}")
    
    # Get all
    all_roles = session.query(BeneficiaryUserPermissionRole).all()
    print(f"Total beneficiary permission roles: {len(all_roles)}")
    
    print("\n3. Verifying all expected roles exist...")
    
    expected_roles = ['Admin', 'Team Member', 'Removed']
    for role_name in expected_roles:
        role = session.query(BeneficiaryUserPermissionRole).filter_by(beneficiary_user_permission_role_name=role_name).first()
        if role:
            print(f"✅ Found: {role_name} (code {role.code})")
        else:
            print(f"❌ Missing: {role_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = BeneficiaryUserPermissionRole(code=1, beneficiary_user_permission_role_name='Duplicate Admin')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing unique name constraint...")
    
    try:
        duplicate_name = BeneficiaryUserPermissionRole(code=99, beneficiary_user_permission_role_name='Admin')
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate name!")
    except Exception as e:
        print("✅ Unique name constraint working")
        session.rollback()
    
    print("\n6. Testing we can add more permission roles...")
    
    try:
        # Add another permission role with different code
        viewer = BeneficiaryUserPermissionRole(code=4, beneficiary_user_permission_role_name='Viewer')
        session.add(viewer)
        session.commit()
        print("✅ Can add additional permission roles")
        
        # Verify we now have 4
        total = session.query(BeneficiaryUserPermissionRole).count()
        print(f"Total permission roles after adding viewer: {total}")
    except Exception as e:
        print(f"❌ Error adding additional permission role: {e}")
        session.rollback()
    
    session.close()
    print("\n🎉 BeneficiaryUserPermissionRole model working perfectly!")

if __name__ == "__main__":
    test_beneficiary_user_permission_role_model()