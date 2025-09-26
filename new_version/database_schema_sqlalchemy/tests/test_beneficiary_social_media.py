"""
Usage: bash python -m database_layer.tests.test_beneficiary_social_media
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.beneficiary_size import BeneficiarySize
from database_layer.src.public.tables.beneficiary import Beneficiary
from database_layer.src.public.tables.social_media_type import SocialMediaType
from database_layer.src.public.tables.beneficiary_social_media import BeneficiarySocialMedia
from .test_utils import create_test_session

def test_beneficiary_social_media_junction():
    print("=== Testing BeneficiarySocialMedia Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create beneficiary size
    medium = BeneficiarySize(code=2, beneficiary_size_name='medium')
    
    # Create social media types
    linkedin = SocialMediaType(code=1, social_media_type_name='linkedin')
    instagram = SocialMediaType(code=2, social_media_type_name='instagram')
    facebook = SocialMediaType(code=3, social_media_type_name='facebook')
    
    session.add_all([medium, linkedin, instagram, facebook])
    session.commit()
    print("✅ Created parent records")
    
    print("\n2. Creating beneficiaries...")
    
    # Create beneficiaries
    green_earth = Beneficiary(
        beneficiary_name='Green Earth Foundation',
        email='contact@greenearth.org',
        location_city='Portland',
        location_state='OR',
        beneficiary_size_id=medium.beneficiary_size_id
    )
    
    local_food = Beneficiary(
        beneficiary_name='Local Food Bank',
        email='info@localfoodbank.org',
        location_city='Denver',
        location_state='CO',
        beneficiary_size_id=medium.beneficiary_size_id
    )
    
    session.add_all([green_earth, local_food])
    session.commit()
    print("✅ Created beneficiaries")
    
    print("\n3. Creating social media links...")
    
    # Green Earth social media
    green_linkedin = BeneficiarySocialMedia(
        beneficiary_id=green_earth.beneficiary_id,
        social_media_type_id=linkedin.social_media_type_id,
        social_media_url='https://linkedin.com/company/greenearth'
    )
    
    green_instagram = BeneficiarySocialMedia(
        beneficiary_id=green_earth.beneficiary_id,
        social_media_type_id=instagram.social_media_type_id,
        social_media_url='https://instagram.com/greenearth'
    )
    
    # Local Food Bank social media
    food_linkedin = BeneficiarySocialMedia(
        beneficiary_id=local_food.beneficiary_id,
        social_media_type_id=linkedin.social_media_type_id,
        social_media_url='https://linkedin.com/company/localfoodbank'
    )
    
    food_facebook = BeneficiarySocialMedia(
        beneficiary_id=local_food.beneficiary_id,
        social_media_type_id=facebook.social_media_type_id,
        social_media_url='https://facebook.com/localfoodbank'
    )
    
    session.add_all([green_linkedin, green_instagram, food_linkedin, food_facebook])
    session.commit()
    print("✅ Created social media links")
    
    print("\n4. Testing relationship navigation...")
    
    # Find all social media for each beneficiary
    green_social = session.query(BeneficiarySocialMedia).filter_by(beneficiary_id=green_earth.beneficiary_id).all()
    print(f"Green Earth has {len(green_social)} social media account(s):")
    for social in green_social:
        print(f"  - {social.social_media_type.social_media_type_name}: {social.social_media_url}")
    
    food_social = session.query(BeneficiarySocialMedia).filter_by(beneficiary_id=local_food.beneficiary_id).all()
    print(f"Local Food Bank has {len(food_social)} social media account(s):")
    for social in food_social:
        print(f"  - {social.social_media_type.social_media_type_name}: {social.social_media_url}")
    
    print("\n5. Testing reverse navigation...")
    
    # Find all beneficiaries on each platform
    linkedin_beneficiaries = session.query(BeneficiarySocialMedia).filter_by(social_media_type_id=linkedin.social_media_type_id).all()
    print(f"LinkedIn has {len(linkedin_beneficiaries)} beneficiary(ies):")
    for ben_social in linkedin_beneficiaries:
        print(f"  - {ben_social.beneficiary.beneficiary_name}")
    
    session.close()
    print("\n🎉 BeneficiarySocialMedia junction table working perfectly!")

if __name__ == "__main__":
    test_beneficiary_social_media_junction()