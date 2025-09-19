"""
Usage: bash python -m database_layer.tests.test_business_size
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_layer.models import Base
from database_layer.models.business_size import BusinessSize

def test_business_size_conversion():
    print("=== Testing BusinessSize Model Conversion ===")
    
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("\n1. Creating the 3 business sizes from your populate_business_size_data.sql...")
    
    # From your populate_business_size_data.sql file:
    # CALL save_business_size(1, 'small');
    # CALL save_business_size(2, 'medium');
    # CALL save_business_size(3, 'large');
    
    small_business = BusinessSize(code=1, business_size_name='small')
    medium_business = BusinessSize(code=2, business_size_name='medium')
    large_business = BusinessSize(code=3, business_size_name='large')
    
    session.add_all([small_business, medium_business, large_business])
    session.commit()
    
    print("\n2. Testing queries...")
    
    all_sizes = session.query(BusinessSize).all()
    print(f"\nTotal business sizes created: {len(all_sizes)}")
    
    for size in all_sizes:
        print(f"  Code {size.code}: {size.business_size_name}")
    
    print("\n3. Testing specific queries...")
    medium = session.query(BusinessSize).filter_by(code=2).first()
    print(f"Medium business size: {medium}")
    
    print("\n4. Testing constraints...")
    try:
        duplicate = BusinessSize(code=1, business_size_name='duplicate small')
        session.add(duplicate)
        session.commit()
        print("❌ ERROR: Should have failed!")
    except Exception:
        print("✅ Unique code constraint working")
        session.rollback()
    
    session.close()
    print("\n🎉 BusinessSize conversion completed successfully!")

if __name__ == "__main__":
    test_business_size_conversion()