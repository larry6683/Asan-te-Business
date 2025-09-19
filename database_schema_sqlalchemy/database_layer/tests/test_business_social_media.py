"""
Usage: bash python -m database_layer.tests.test_business_social_media
"""
import uuid
from sqlalchemy.sql import func
from database_layer.models.business_size import BusinessSize
from database_layer.models.business import Business
from database_layer.models.social_media_type import SocialMediaType
from database_layer.models.business_social_media import BusinessSocialMedia
from .test_utils import create_test_session

def test_business_social_media_junction():
    print("=== Testing BusinessSocialMedia Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create business size
    medium = BusinessSize(code=2, business_size_name='medium')
    
    # Create social media types
    linkedin = SocialMediaType(code=1, social_media_type_name='linkedin')
    instagram = SocialMediaType(code=2, social_media_type_name='instagram')
    facebook = SocialMediaType(code=3, social_media_type_name='facebook')
    
    session.add_all([medium, linkedin, instagram, facebook])
    session.commit()
    print("✅ Created parent records")
    
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
        business_size_id=medium.business_size_id
    )
    
    session.add_all([eco_solutions, tech_innovations])
    session.commit()
    print("✅ Created businesses")
    
    print("\n3. Creating social media links...")
    
    # Eco Solutions social media
    eco_linkedin = BusinessSocialMedia(
        business_id=eco_solutions.business_id,
        social_media_type_id=linkedin.social_media_type_id,
        social_media_url='https://linkedin.com/company/ecosolutions'
    )
    
    eco_instagram = BusinessSocialMedia(
        business_id=eco_solutions.business_id,
        social_media_type_id=instagram.social_media_type_id,
        social_media_url='https://instagram.com/ecosolutions'
    )
    
    # Tech Innovations social media
    tech_linkedin = BusinessSocialMedia(
        business_id=tech_innovations.business_id,
        social_media_type_id=linkedin.social_media_type_id,
        social_media_url='https://linkedin.com/company/techinnovations'
    )
    
    tech_facebook = BusinessSocialMedia(
        business_id=tech_innovations.business_id,
        social_media_type_id=facebook.social_media_type_id,
        social_media_url='https://facebook.com/techinnovations'
    )
    
    session.add_all([eco_linkedin, eco_instagram, tech_linkedin, tech_facebook])
    session.commit()
    print("✅ Created social media links")
    
    print("\n4. Testing relationship navigation...")
    
    # Find all social media for each business
    eco_social = session.query(BusinessSocialMedia).filter_by(business_id=eco_solutions.business_id).all()
    print(f"Eco Solutions has {len(eco_social)} social media account(s):")
    for social in eco_social:
        print(f"  - {social.social_media_type.social_media_type_name}: {social.social_media_url}")
    
    tech_social = session.query(BusinessSocialMedia).filter_by(business_id=tech_innovations.business_id).all()
    print(f"Tech Innovations has {len(tech_social)} social media account(s):")
    for social in tech_social:
        print(f"  - {social.social_media_type.social_media_type_name}: {social.social_media_url}")
    
    print("\n5. Testing reverse navigation...")
    
    # Find all businesses on each platform
    linkedin_businesses = session.query(BusinessSocialMedia).filter_by(social_media_type_id=linkedin.social_media_type_id).all()
    print(f"LinkedIn has {len(linkedin_businesses)} business(es):")
    for biz_social in linkedin_businesses:
        print(f"  - {biz_social.business.business_name}")
    
    instagram_businesses = session.query(BusinessSocialMedia).filter_by(social_media_type_id=instagram.social_media_type_id).all()
    print(f"Instagram has {len(instagram_businesses)} business(es):")
    for biz_social in instagram_businesses:
        print(f"  - {biz_social.business.business_name}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create social media with invalid business_id
    try:
        bad_business_social = BusinessSocialMedia(
            business_id=uuid.uuid4(),  # Random UUID that doesn't exist
            social_media_type_id=linkedin.social_media_type_id,
            social_media_url='https://linkedin.com/company/bad'
        )
        session.add(bad_business_social)
        session.commit()
        print("❌ ERROR: Should have failed due to business foreign key constraint!")
    except Exception as e:
        print("✅ Business foreign key constraint working")
        session.rollback()
    
    # Try to create social media with invalid social_media_type_id
    try:
        bad_type_social = BusinessSocialMedia(
            business_id=eco_solutions.business_id,
            social_media_type_id=uuid.uuid4(),  # Random UUID that doesn't exist
            social_media_url='https://badplatform.com/ecosolutions'
        )
        session.add(bad_type_social)
        session.commit()
        print("❌ ERROR: Should have failed due to social media type foreign key constraint!")
    except Exception as e:
        print("✅ Social media type foreign key constraint working")
        session.rollback()
    
    print("\n7. Testing queries...")
    
    # Count social media by platform
    for platform in [linkedin, instagram, facebook]:
        count = session.query(BusinessSocialMedia).filter_by(social_media_type_id=platform.social_media_type_id).count()
        print(f"{platform.social_media_type_name.title()} accounts: {count}")
    
    # Find businesses with multiple social media accounts
    businesses_with_multiple = session.query(BusinessSocialMedia.business_id).group_by(BusinessSocialMedia.business_id).having(func.count() > 1).all()
    print(f"Businesses with multiple social media accounts: {len(businesses_with_multiple)}")
    
    session.close()
    print("\n🎉 BusinessSocialMedia junction table working perfectly!")

if __name__ == "__main__":
    test_business_social_media_junction()