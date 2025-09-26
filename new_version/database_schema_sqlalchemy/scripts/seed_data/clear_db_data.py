
"""
Clear all seed/test data for development.
This replaces clear_db_data.sql script used by reset_seed_data.sh.

Unlike delete_seed_data.py, this clears ALL data from transactional tables,
not just specific test records.
"""

import sys
import os

# Add the project root to Python path to import database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_layer.src.public.tables import (
    Base, Business, AppUser, BusinessUser, BusinessSocialMedia,
    BusinessCausePreference, BusinessShop, BusinessImpactLink,
    Beneficiary, BeneficiaryUser, BeneficiarySocialMedia, 
    BeneficiaryCausePreference, BeneficiaryShop
)

def create_session(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """Create database session"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def clear_db_data(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """
    Clear all transactional data - equivalent to clear_db_data.sql
    
    This removes ALL data from business and beneficiary tables,
    but preserves reference data (user_types, business_sizes, causes, etc.)
    """
    print("Clearing all seed/test data...")
    
    try:
        engine, session = create_session(database_url)
        
        # Delete in correct order (children first, then parents)
        # Same order as original clear_db_data.sql
        
        print("Deleting beneficiary data...")
        session.query(BeneficiaryShop).delete(synchronize_session=False)
        session.query(BeneficiarySocialMedia).delete(synchronize_session=False)
        session.query(BeneficiaryCausePreference).delete(synchronize_session=False)
        session.query(BeneficiaryUser).delete(synchronize_session=False)
        session.query(Beneficiary).delete(synchronize_session=False)
        
        print("Deleting business data...")
        session.query(BusinessImpactLink).delete(synchronize_session=False)
        session.query(BusinessShop).delete(synchronize_session=False)
        session.query(BusinessSocialMedia).delete(synchronize_session=False)
        session.query(BusinessCausePreference).delete(synchronize_session=False)
        session.query(BusinessUser).delete(synchronize_session=False)
        session.query(Business).delete(synchronize_session=False)
        
        print("Deleting app users...")
        session.query(AppUser).delete(synchronize_session=False)
        
        # Commit all deletions
        session.commit()
        session.close()
        
        print("All seed data cleared successfully!")
        print("Preserved reference data:")
        print("- User types, business sizes, beneficiary sizes")
        print("- Causes, cause categories, cause preference ranks")
        print("- Social media types, shop types")
        print("- Permission roles, registration types")
        
    except Exception as e:
        print(f"Error clearing data: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise

if __name__ == "__main__":
    clear_db_data()