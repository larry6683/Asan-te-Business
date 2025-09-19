"""
Usage: bash python -m database_layer.tests.test_user_type
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import from the package structure
from database_layer.models import Base, UserType

def test_user_type_conversion():
    print("=== Testing UserType Model Conversion ===")
    
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("\n1. Creating the 3 user types...")
    
    business_user = UserType(code=1, user_type_name='business user')
    beneficiary_user = UserType(code=2, user_type_name='beneficiary user')
    consumer_user = UserType(code=3, user_type_name='consumer user')
    
    session.add_all([business_user, beneficiary_user, consumer_user])
    session.commit()
    
    print("\n2. Testing queries...")
    
    all_types = session.query(UserType).all()
    print(f"\nTotal user types created: {len(all_types)}")
    
    for user_type in all_types:
        print(f"  Code {user_type.code}: {user_type.user_type_name}")
    
    print("\n🎉 UserType conversion completed successfully!")
    session.close()

if __name__ == "__main__":
    test_user_type_conversion()