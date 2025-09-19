# test_api_integration.py
"""
Test script to verify SQLAlchemy models work for gRPC API integration.

"""

import sys
import os

# Add the current directory to Python path to database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_layer.models import *

def test_models_import():
    """Test that all models can be imported successfully"""
    print("Testing model imports...")
    
    key_models = [
        # User tables
        'UserType', 'AppUser', 'RegistrationType', 'AppUserRegistrationType',
        
        # Domain/System type data
        'CauseCategory', 'Cause', 'CausePreferenceRank', 'SocialMediaType', 'ShopType',
        
        # Business tables
        'BusinessSize', 'BusinessUserPermissionRole', 'BusinessType', 'Business',
        'BusinessUser', 'BusinessCausePreference', 'BusinessSocialMedia',
        'BusinessShop', 'BusinessImpactLink',
        
        # Beneficiary tables
        'BeneficiarySize', 'BeneficiaryUserPermissionRole', 'BeneficiaryType',
        'Beneficiary', 'BeneficiaryUser', 'BeneficiaryCausePreference',
        'BeneficiarySocialMedia', 'BeneficiaryShop'
    ]
    
    print(f"Testing {len(key_models)} key models...")
    for model_name in key_models:
        try:
            model_class = globals()[model_name]
            print(f"✅ {model_name} imported successfully")
        except KeyError:
            print(f"❌ {model_name} not found!")
    
    print("All models imported successfully using 'from database_layer.models import *'!")

def test_database_connection_and_queries():
    """Test database connection and basic queries your teammate might use"""
    print("\nTesting database connection and queries...")
    
    # Database connection 
    database_url = "postgresql://asante_dev:password@localhost:5432/postgres"
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Test 1: Get all user types (for user registration)
        print("\n1. Testing user type queries:")
        user_types = session.query(UserType).all()
        for user_type in user_types:
            print(f"   - {user_type.user_type_name} (code: {user_type.code})")
        
        # Test 2: Get registration types
        print("\n2. Testing registration types:")
        reg_types = session.query(RegistrationType).all()
        for reg_type in reg_types:
            print(f"   - {reg_type.registration_type_name} (code: {reg_type.code})")
        
        # Test 3: Get business sizes
        print("\n3. Testing business sizes:")
        business_sizes = session.query(BusinessSize).all()
        for size in business_sizes:
            print(f"   - {size.business_size_name} (code: {size.code})")
        
        # Test 4: Get causes by category
        print("\n4. Testing causes and categories:")
        causes = session.query(Cause).join(CauseCategory).limit(5).all()
        for cause in causes:
            print(f"   - {cause.cause_name} ({cause.cause_category.cause_category_name})")
        
        # Test 5: Get business user for authentication
        print("\n5. Testing user authentication query:")
        sample_user = session.query(AppUser).filter_by(email='admin1@business1.com').first()
        if sample_user:
            print(f"   Found user: {sample_user.email}")
            print(f"   User type: {sample_user.user_type.user_type_name}")
        
        # Test 6: Get business details (for business profile)
        print("\n6. Testing business profile query:")
        business = session.query(Business).filter_by(business_name='Eco Solutions Inc.').first()
        if business:
            print(f"   Business: {business.business_name}")
            print(f"   Location: {business.location_city}, {business.location_state}")
            print(f"   Size: {business.business_size.business_size_name}")
            
            # Get business users
            business_users = session.query(BusinessUser).filter_by(business_id=business.business_id).all()
            print(f"   Users: {len(business_users)}")
            for bu in business_users:
                print(f"     - {bu.app_user.email} ({bu.permission_role.business_user_permission_role_name})")
        
        # Test 7: Create a new user (for user registration endpoint)
        print("\n7. Testing user creation:")
        business_user_type = session.query(UserType).filter_by(code=1).first()
        
        new_user = AppUser(
            user_type_id=business_user_type.user_type_id,
            email='test@newcompany.com',
            mailing_list_signup=True
        )
        
        session.add(new_user)
        session.commit()
        print(f"   ✅ Created new user: {new_user.email}")
        print(f"   User ID: {new_user.app_user_id}")
        
        # Clean up test user
        session.delete(new_user)
        session.commit()
        print("   ✅ Cleaned up test user")
        
        # Test 8: Count all the important tables
        print("\n8. Testing table counts:")
        counts = {
            'User Types': session.query(UserType).count(),
            'App Users': session.query(AppUser).count(),
            'Registration Types': session.query(RegistrationType).count(),
            'Business Sizes': session.query(BusinessSize).count(),
            'Businesses': session.query(Business).count(),
            'Business Users': session.query(BusinessUser).count(),
            'Cause Categories': session.query(CauseCategory).count(),
            'Causes': session.query(Cause).count(),
            'Social Media Types': session.query(SocialMediaType).count(),
            'Shop Types': session.query(ShopType).count()
        }
        
        for table_name, count in counts.items():
            print(f"   - {table_name}: {count}")
        
        session.close()
        print("\n🎉 All database tests passed! Your models are ready for API integration.")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        session.rollback()
        session.close()
        return False

def example_api_usage():
    """Show examples of how your teammate can use these models in the API"""
    print("\n" + "="*60)
    print("EXAMPLE: How to use these models in your gRPC API")
    print("="*60)
    
    example_code = '''
# In your gRPC service file, import ALL models:
from database_layer.models import *

# Create database session:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://asante_dev:password@localhost:5432/postgres")
Session = sessionmaker(bind=engine)

# Example 1: User registration endpoint
def create_user(request, context):
    session = Session()
    try:
        # Get business user type
        business_user_type = session.query(UserType).filter_by(code=1).first()
        
        # Create new user
        new_user = AppUser(
            user_type_id=business_user_type.user_type_id,
            email=request.email,
            mailing_list_signup=request.mailing_list_signup
        )
        
        session.add(new_user)
        session.commit()
        
        return CreateUserResponse(
            user_id=str(new_user.app_user_id),
            email=new_user.email,
            success=True
        )
    except Exception as e:
        session.rollback()
        return CreateUserResponse(success=False, error=str(e))
    finally:
        session.close()

# Example 2: Get user endpoint  
def get_user(request, context):
    session = Session()
    try:
        user = session.query(AppUser).filter_by(app_user_id=request.user_id).first()
        
        if user:
            return GetUserResponse(
                user_id=str(user.app_user_id),
                email=user.email,
                user_type=user.user_type.user_type_name,
                success=True
            )
        else:
            return GetUserResponse(success=False, error="User not found")
    finally:
        session.close()

# Example 3: Business registration
def create_business(request, context):
    session = Session()
    try:
        # Get business size
        business_size = session.query(BusinessSize).filter_by(code=request.size_code).first()
        
        # Create business
        new_business = Business(
            business_name=request.business_name,
            email=request.email,
            location_city=request.city,
            location_state=request.state,
            business_size_id=business_size.business_size_id
        )
        
        session.add(new_business)
        session.commit()
        
        return CreateBusinessResponse(
            business_id=str(new_business.business_id),
            success=True
        )
    except Exception as e:
        session.rollback()
        return CreateBusinessResponse(success=False, error=str(e))
    finally:
        session.close()
'''
    
    print(example_code)

if __name__ == "__main__":
    print("🧪 Testing SQLAlchemy Models for API Integration")
    print("=" * 60)
    
    # Test imports
    test_models_import()
    
    # Test database operations
    success = test_database_connection_and_queries()
    
    if success:
        # Show usage examples
        example_api_usage()
        
        print("\n  SQLAlchemy models are ready")
  
    else:
        print("\n❌ Models not ready - fix database issues first")
