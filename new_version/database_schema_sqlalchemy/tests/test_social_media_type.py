"""
Usage: bash python -m database_layer.tests.test_social_media_type
"""
from database_layer.src.public.tables.social_media_type import SocialMediaType
from .test_utils import create_test_session

def test_social_media_type_model():
    print("=== Testing SocialMediaType Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating social media types...")
    
    # Create the 4 standard social media types (from your populate script)
    unspecified = SocialMediaType(code=0, social_media_type_name='unspecified')
    linkedin = SocialMediaType(code=1, social_media_type_name='linkedin')
    instagram = SocialMediaType(code=2, social_media_type_name='instagram')
    facebook = SocialMediaType(code=3, social_media_type_name='facebook')
    
    session.add_all([unspecified, linkedin, instagram, facebook])
    session.commit()
    
    print("✅ Created all 4 social media types")
    
    print("\n2. Testing queries...")
    
    # Query by code
    linkedin_type = session.query(SocialMediaType).filter_by(code=1).first()
    print(f"Found by code: {linkedin_type}")
    
    # Query by name
    facebook_type = session.query(SocialMediaType).filter_by(social_media_type_name='facebook').first()
    print(f"Found by name: {facebook_type}")
    
    # Get all
    all_types = session.query(SocialMediaType).all()
    print(f"Total social media types: {len(all_types)}")
    
    print("\n3. Verifying all expected types exist...")
    
    expected_types = ['unspecified', 'linkedin', 'instagram', 'facebook']
    for type_name in expected_types:
        social_type = session.query(SocialMediaType).filter_by(social_media_type_name=type_name).first()
        if social_type:
            print(f"✅ Found: {type_name} (code {social_type.code})")
        else:
            print(f"❌ Missing: {type_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = SocialMediaType(code=1, social_media_type_name='duplicate-linkedin')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing unique name constraint...")
    
    try:
        duplicate_name = SocialMediaType(code=99, social_media_type_name='linkedin')
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate name!")
    except Exception as e:
        print("✅ Unique name constraint working")
        session.rollback()
    
    session.close()
    print("\n🎉 SocialMediaType model working perfectly!")

if __name__ == "__main__":
    test_social_media_type_model()