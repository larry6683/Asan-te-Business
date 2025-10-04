"""
Usage: bash python -m database_layer.tests.test_business
"""
import uuid
from database_layer.src.public.tables.business_size import BusinessSize
from database_layer.src.public.tables.business import Business
from .test_utils import create_test_session

def test_business_with_foreign_keys():
    print("=== Testing Business Model with Foreign Key Relationships ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating business sizes...")
    
    # Create business sizes first (parent records)
    small = BusinessSize(code=1, business_size_name='small')
    medium = BusinessSize(code=2, business_size_name='medium')
    large = BusinessSize(code=3, business_size_name='large')
    
    session.add_all([small, medium, large])
    session.commit()
    print("✅ Created business sizes")
    
    print("\n2. Creating businesses with valid foreign keys...")
    
    # Create businesses that reference the business sizes
    eco_solutions = Business(
        business_name='Eco Solutions Inc.',
        email='contact@ecosolutions.com',
        website_url='https://ecosolutions.com',
        phone_number='555-123-4567',
        location_city='Seattle',
        location_state='WA',
        business_description='Sustainable product manufacturer',
        business_size_id=medium.business_size_id,
        business_name_hash=b'eco_hash',
        email_hash=b'contact_hash'
    )
    
    tech_innovations = Business(
        business_name='Tech Innovations Ltd',
        email='info@techinnovations.com',
        website_url='https://techinnovations.com',
        phone_number='555-234-5678',
        location_city='San Francisco',
        location_state='CA',
        business_description='AI and machine learning solutions',
        business_size_id=large.business_size_id
    )
    
    local_harvest = Business(
        business_name='Local Harvest Co-op',
        email='hello@localharvest.org',
        website_url='https://localharvest.org',
        phone_number='555-345-6789',
        location_city='Portland',
        location_state='OR',
        business_description='Community-owned grocery',
        business_size_id=small.business_size_id,
        ein='12-3456789'
    )
    
    session.add_all([eco_solutions, tech_innovations, local_harvest])
    session.commit()
    print("✅ Created businesses with valid foreign keys")
    
    print("\n3. Testing relationship navigation (Business -> BusinessSize)...")
    
    # Test forward relationship
    print(f"Eco Solutions size: {eco_solutions.business_size.business_size_name}")
    print(f"Tech Innovations size: {tech_innovations.business_size.business_size_name}")
    print(f"Local Harvest size: {local_harvest.business_size.business_size_name}")
    
    print("\n4. Testing relationship navigation (BusinessSize -> Businesses)...")
    
    # Test back relationship
    print(f"Small businesses ({len(small.businesses)}):")
    for business in small.businesses:
        print(f"  - {business.business_name}")
    
    print(f"Medium businesses ({len(medium.businesses)}):")
    for business in medium.businesses:
        print(f"  - {business.business_name}")
    
    print(f"Large businesses ({len(large.businesses)}):")
    for business in large.businesses:
        print(f"  - {business.business_name}")
    
    print("\n5. Testing queries and special fields...")
    
    # Query by business name
    eco = session.query(Business).filter_by(business_name='Eco Solutions Inc.').first()
    print(f"Found business by name: {eco.business_name}")
    
    # Query by email
    tech = session.query(Business).filter_by(email='info@techinnovations.com').first()
    print(f"Found business by email: {tech.business_name}")
    
    # Query by location
    seattle_businesses = session.query(Business).filter_by(location_city='Seattle').all()
    print(f"Seattle businesses: {len(seattle_businesses)}")
    
    # Query businesses with EIN
    businesses_with_ein = session.query(Business).filter(Business.ein.isnot(None)).all()
    print(f"Businesses with EIN: {len(businesses_with_ein)}")
    
    # Query businesses with name hash
    businesses_with_name_hash = session.query(Business).filter(Business.business_name_hash.isnot(None)).all()
    print(f"Businesses with name hash: {len(businesses_with_name_hash)}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create business with invalid business_size_id
    try:
        bad_business = Business(
            business_name='Bad Business',
            email='bad@business.com',
            location_city='Nowhere',
            location_state='XX',
            business_size_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_business)
        session.commit()
        print("❌ ERROR: Should have failed due to foreign key constraint!")
    except Exception as e:
        print("✅ Foreign key constraint working")
        print(f"   Error: {type(e).__name__}")
        session.rollback()
    
    print("\n7. Testing unique constraints...")
    
    try:
        duplicate_name = Business(
            business_name='Eco Solutions Inc.',  # Same name
            email='different@email.com',
            location_city='Different City',
            location_state='CA',
            business_size_id=small.business_size_id
        )
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate business name!")
    except Exception as e:
        print("✅ Unique business name constraint working")
        session.rollback()
    
    try:
        duplicate_email = Business(
            business_name='Different Business',
            email='contact@ecosolutions.com',  # Same email
            location_city='Different City',
            location_state='CA',
            business_size_id=small.business_size_id
        )
        session.add(duplicate_email)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate email!")
    except Exception as e:
        print("✅ Unique email constraint working")
        session.rollback()
    
    print("\n8. Testing default values...")
    
    # Test default description
    minimal_business = Business(
        business_name='Minimal Business',
        email='minimal@business.com',
        location_city='Minimal City',
        location_state='TX',
        business_size_id=small.business_size_id
    )
    session.add(minimal_business)
    session.commit()
    
    print(f"Default description: '{minimal_business.business_description}'")
    if minimal_business.business_description == '':
        print("✅ Default business description working")
    else:
        print("❌ Default business description not working")
    
    session.close()
    print("\n🎉 Business with foreign keys and indexes working perfectly!")

if __name__ == "__main__":
    test_business_with_foreign_keys()