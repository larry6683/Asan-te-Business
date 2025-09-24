"""
Usage: bash python -m database_layer.tests.test_cause_category
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_layer.models import Base
from database_layer.models.cause_category import CauseCategory

def test_cause_category_conversion():
    print("=== Testing CauseCategory Model Conversion ===")
    
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("\n1. Creating the 5 cause categories from your populate data...")
    
    # From your populate_cause_and_cause_category_data.sql:
    # CALL save_cause_category(1, 'Community');
    # CALL save_cause_category(2, 'Social');
    # CALL save_cause_category(3, 'Innovation');
    # CALL save_cause_category(4, 'Environment');
    # CALL save_cause_category(5, 'Emergency Relief');
    
    community = CauseCategory(code=1, cause_category_name='Community')
    social = CauseCategory(code=2, cause_category_name='Social')
    innovation = CauseCategory(code=3, cause_category_name='Innovation')
    environment = CauseCategory(code=4, cause_category_name='Environment')
    emergency_relief = CauseCategory(code=5, cause_category_name='Emergency Relief')
    
    session.add_all([community, social, innovation, environment, emergency_relief])
    session.commit()
    
    print("\n2. Testing queries...")
    
    all_categories = session.query(CauseCategory).all()
    print(f"\nTotal cause categories created: {len(all_categories)}")
    
    for category in all_categories:
        print(f"  Code {category.code}: {category.cause_category_name}")
    
    print("\n3. Testing specific queries...")
    
    # Test finding by code
    environment_cat = session.query(CauseCategory).filter_by(code=4).first()
    print(f"Environment category: {environment_cat}")
    
    # Test finding by name
    social_cat = session.query(CauseCategory).filter_by(cause_category_name='Social').first()
    print(f"Social category: {social_cat}")
    
    print("\n4. Testing constraints...")
    
    # Test unique code constraint
    try:
        duplicate_code = CauseCategory(code=1, cause_category_name='Duplicate Community')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        print(f"   Error: {type(e).__name__}")
        session.rollback()
    
    # Test unique name constraint
    try:
        duplicate_name = CauseCategory(code=6, cause_category_name='Community')
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate name!")
    except Exception as e:
        print("✅ Unique name constraint working")
        print(f"   Error: {type(e).__name__}")
        session.rollback()
    
    print("\n5. Testing data integrity...")
    
    # Verify we can query all expected categories
    expected_categories = ['Community', 'Social', 'Innovation', 'Environment', 'Emergency Relief']
    for expected_name in expected_categories:
        found = session.query(CauseCategory).filter_by(cause_category_name=expected_name).first()
        if found:
            print(f"✅ Found {expected_name} (code {found.code})")
        else:
            print(f"❌ Missing {expected_name}")
    
    session.close()
    print("\n🎉 CauseCategory conversion completed successfully!")

if __name__ == "__main__":
    test_cause_category_conversion()