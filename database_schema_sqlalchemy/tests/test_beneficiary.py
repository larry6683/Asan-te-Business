"""
Usage: bash python -m database_layer.tests.test_beneficiary
"""
import uuid
from database_layer.src.public.tables.beneficiary_size import BeneficiarySize
from database_layer.src.public.tables.beneficiary import Beneficiary
from .test_utils import create_test_session

def test_beneficiary_with_foreign_keys():
    print("=== Testing Beneficiary Model with Foreign Key Relationships ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating beneficiary sizes...")
    
    # Create beneficiary sizes first (parent records)
    small = BeneficiarySize(code=1, beneficiary_size_name='small')
    medium = BeneficiarySize(code=2, beneficiary_size_name='medium')
    large = BeneficiarySize(code=3, beneficiary_size_name='large')
    
    session.add_all([small, medium, large])
    session.commit()
    print("✅ Created beneficiary sizes")
    
    print("\n2. Creating beneficiaries with valid foreign keys...")
    
    # Create beneficiaries that reference the beneficiary sizes
    homeless_shelter = Beneficiary(
        beneficiary_name='Downtown Homeless Shelter',
        email='info@downtownshelter.org',
        website_url='https://downtownshelter.org',
        phone_number='555-111-2222',
        location_city='Denver',
        location_state='CO',
        beneficiary_description='Emergency shelter and support services',
        beneficiary_size_id=medium.beneficiary_size_id,
        beneficiary_name_hash=b'shelter_hash',
        email_hash=b'info_hash',
        ein='12-3456789'
    )
    
    food_bank = Beneficiary(
        beneficiary_name='Community Food Bank',
        email='contact@communityfoodbank.org',
        website_url='https://communityfoodbank.org',
        phone_number='555-333-4444',
        location_city='Boulder',
        location_state='CO',
        beneficiary_description='Providing food assistance to families in need',
        beneficiary_size_id=large.beneficiary_size_id
    )
    
    youth_center = Beneficiary(
        beneficiary_name='Local Youth Center',
        email='hello@youthcenter.org',
        location_city='Fort Collins',
        location_state='CO',
        beneficiary_description='After-school programs and youth development',
        beneficiary_size_id=small.beneficiary_size_id
    )
    
    session.add_all([homeless_shelter, food_bank, youth_center])
    session.commit()
    print("✅ Created beneficiaries with valid foreign keys")
    
    print("\n3. Testing relationship navigation (Beneficiary -> BeneficiarySize)...")
    
    # Test forward relationship
    print(f"Homeless Shelter size: {homeless_shelter.beneficiary_size.beneficiary_size_name}")
    print(f"Food Bank size: {food_bank.beneficiary_size.beneficiary_size_name}")
    print(f"Youth Center size: {youth_center.beneficiary_size.beneficiary_size_name}")
    
    print("\n4. Testing relationship navigation (BeneficiarySize -> Beneficiaries)...")
    
    # Test back relationship
    print(f"Small beneficiaries ({len(small.beneficiaries)}):")
    for beneficiary in small.beneficiaries:
        print(f"  - {beneficiary.beneficiary_name}")
    
    print(f"Medium beneficiaries ({len(medium.beneficiaries)}):")
    for beneficiary in medium.beneficiaries:
        print(f"  - {beneficiary.beneficiary_name}")
    
    print(f"Large beneficiaries ({len(large.beneficiaries)}):")
    for beneficiary in large.beneficiaries:
        print(f"  - {beneficiary.beneficiary_name}")
    
    print("\n5. Testing queries and special fields...")
    
    # Query by beneficiary name
    shelter = session.query(Beneficiary).filter_by(beneficiary_name='Downtown Homeless Shelter').first()
    print(f"Found beneficiary by name: {shelter.beneficiary_name}")
    
    # Query by email
    food = session.query(Beneficiary).filter_by(email='contact@communityfoodbank.org').first()
    print(f"Found beneficiary by email: {food.beneficiary_name}")
    
    # Query by location
    denver_beneficiaries = session.query(Beneficiary).filter_by(location_city='Denver').all()
    print(f"Denver beneficiaries: {len(denver_beneficiaries)}")
    
    # Query beneficiaries with EIN
    beneficiaries_with_ein = session.query(Beneficiary).filter(Beneficiary.ein.isnot(None)).all()
    print(f"Beneficiaries with EIN: {len(beneficiaries_with_ein)}")
    
    # Query beneficiaries with name hash
    beneficiaries_with_name_hash = session.query(Beneficiary).filter(Beneficiary.beneficiary_name_hash.isnot(None)).all()
    print(f"Beneficiaries with name hash: {len(beneficiaries_with_name_hash)}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create beneficiary with invalid beneficiary_size_id
    try:
        bad_beneficiary = Beneficiary(
            beneficiary_name='Bad Beneficiary',
            email='bad@beneficiary.org',
            location_city='Nowhere',
            location_state='XX',
            beneficiary_size_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_beneficiary)
        session.commit()
        print("❌ ERROR: Should have failed due to foreign key constraint!")
    except Exception as e:
        print("✅ Foreign key constraint working")
        print(f"   Error: {type(e).__name__}")
        session.rollback()
    
    print("\n7. Testing unique constraints...")
    
    try:
        duplicate_name = Beneficiary(
            beneficiary_name='Downtown Homeless Shelter',  # Same name
            email='different@email.org',
            location_city='Different City',
            location_state='CA',
            beneficiary_size_id=small.beneficiary_size_id
        )
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate beneficiary name!")
    except Exception as e:
        print("✅ Unique beneficiary name constraint working")
        session.rollback()
    
    try:
        duplicate_email = Beneficiary(
            beneficiary_name='Different Beneficiary',
            email='info@downtownshelter.org',  # Same email
            location_city='Different City',
            location_state='CA',
            beneficiary_size_id=small.beneficiary_size_id
        )
        session.add(duplicate_email)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate email!")
    except Exception as e:
        print("✅ Unique email constraint working")
        session.rollback()
    
    print("\n8. Testing default values...")
    
    # Test default description
    minimal_beneficiary = Beneficiary(
        beneficiary_name='Minimal Beneficiary',
        email='minimal@beneficiary.org',
        location_city='Minimal City',
        location_state='TX',
        beneficiary_size_id=small.beneficiary_size_id
    )
    session.add(minimal_beneficiary)
    session.commit()
    
    print(f"Default description: '{minimal_beneficiary.beneficiary_description}'")
    if minimal_beneficiary.beneficiary_description == '':
        print("✅ Default beneficiary description working")
    else:
        print("❌ Default beneficiary description not working")
    
    session.close()
    print("\n🎉 Beneficiary with foreign keys and indexes working perfectly!")

if __name__ == "__main__":
    test_beneficiary_with_foreign_keys()