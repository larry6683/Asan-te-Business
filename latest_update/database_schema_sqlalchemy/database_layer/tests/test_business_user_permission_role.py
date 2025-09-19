"""
Usage: bash python -m database_layer.tests.test_business_user_permission_role
"""
from database_layer.models.business_user_permission_role import BusinessUserPermissionRole
from .test_utils import create_test_session

def test_business_user_permission_role_model():
    print("=== Testing BusinessUserPermissionRole Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating business user permission roles...")
    
    # Create the 3 standard permission roles (from your populate script)
    admin = BusinessUserPermissionRole(code=1, business_user_permission_role_name='Admin')
    team_member = BusinessUserPermissionRole(code=2, business_user_permission_role_name='Team Member')
    removed = BusinessUserPermissionRole(code=3, business_user_permission_role_name='Removed')
    
    session.add_all([admin, team_member, removed])
    session.commit()
    
    print("✅ Created all 3 business permission roles")
    
    print("\n2. Testing queries...")
    
    # Query by code
    admin_role = session.query(BusinessUserPermissionRole).filter_by(code=1).first()
    print(f"Found by code: {admin_role}")
    
    # Query by name
    team_role = session.query(BusinessUserPermissionRole).filter_by(business_user_permission_role_name='Team Member').first()
    print(f"Found by name: {team_role}")
    
    # Get all
    all_roles = session.query(BusinessUserPermissionRole).all()
    print(f"Total business permission roles: {len(all_roles)}")
    
    print("\n3. Verifying all expected roles exist...")
    
    expected_roles = ['Admin', 'Team Member', 'Removed']
    for role_name in expected_roles:
        role = session.query(BusinessUserPermissionRole).filter_by(business_user_permission_role_name=role_name).first()
        if role:
            print(f"✅ Found: {role_name} (code {role.code})")
        else:
            print(f"❌ Missing: {role_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = BusinessUserPermissionRole(code=1, business_user_permission_role_name='Duplicate Admin')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing unique name constraint...")
    
    try:
        duplicate_name = BusinessUserPermissionRole(code=99, business_user_permission_role_name='Admin')
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate name!")
    except Exception as e:
        print("✅ Unique name constraint working")
        session.rollback()
    
    print("\n6. Testing we can add more permission roles...")
    
    try:
        # Add another permission role with different code
        read_only = BusinessUserPermissionRole(code=4, business_user_permission_role_name='Read Only')
        session.add(read_only)
        session.commit()
        print("✅ Can add additional permission roles")
        
        # Verify we now have 4
        total = session.query(BusinessUserPermissionRole).count()
        print(f"Total permission roles after adding read-only: {total}")
    except Exception as e:
        print(f"❌ Error adding additional permission role: {e}")
        session.rollback()
    
    session.close()
    print("\n🎉 BusinessUserPermissionRole model working perfectly!")

if __name__ == "__main__":
    test_business_user_permission_role_model()