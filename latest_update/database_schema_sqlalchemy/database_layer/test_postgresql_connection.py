"""
PostgreSQL Connection Test Script

Originally created to test SQLAlchemy model connectivity against database 
populated with raw SQL (before SQLAlchemy setup existed). Now can serve as:
- Alternative connection verification tool
- Simple validation after setup_database.py

PREREQUISITES: Docker PostgreSQL running, database populated (either with raw SQL or SQLAlchemy)

Run: python database_layer/test_postgresql_connection.py
"""

from models.base import Base
from models.business import Business
from models.app_user import AppUser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_postgresql_connection():
    print("=== Testing PostgreSQL Connection ===")
    
    # Connect to your PostgreSQL database
    engine = create_engine('postgresql://asante_dev:password@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Test: Can we query existing data?
        businesses = session.query(Business).all()
        print(f"Found {len(businesses)} businesses in PostgreSQL")
        
        # Show some business names
        for business in businesses[:3]: 
            print(f"  - {business.business_name}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def test_relationships():
    print("\n=== Testing Relationships ===")
    
    engine = create_engine('postgresql://asante_dev:password@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Test business social media relationships  
        businesses = session.query(Business).all()
        for business in businesses:
            print(f"\n{business.business_name}:")
            for social in business.social_media: 
                print(f"  - {social.social_media_type.social_media_type_name}: {social.social_media_url}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    test_postgresql_connection()
    test_relationships() 