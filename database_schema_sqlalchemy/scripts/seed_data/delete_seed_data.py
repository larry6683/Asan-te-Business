"""
Delete specific test/seed data for development.
This replaces delete_seed_data.sql script.
Unlike clear_db_data.py, this only deletes the specific test records created by public_seed_data.py,
not ALL data from transactional tables.
"""

import sys
import os
import uuid

# Add the project root to Python path to import database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_layer.src.public.tables import (
    Base, Business, AppUser, BusinessUser, BusinessSocialMedia,
    BusinessCausePreference, BusinessShop, BusinessImpactLink
)

def create_session(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """Create database session"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def delete_seed_data(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """
    Delete specific test data created by public_seed_data.py - equivalent to delete_seed_data.sql
    This removes only the 3 specific test businesses and 12 test users,
    leaving other data intact.
    """
    print("Deleting specific seed data...")
    
    try:
        engine, session = create_session(database_url)
        
        # Pre-defined UUIDs that match public_seed_data.py exactly
        business_ids = [
            'b1111111-1111-1111-1111-111111111111',
            'b2222222-2222-2222-2222-222222222222', 
            'b3333333-3333-3333-3333-333333333333'
        ]
        
        app_user_ids = [
            # Business 1 Users
            '11111111-1111-1111-1111-111111111101',
            '11111111-1111-1111-1111-111111111102',
            '11111111-1111-1111-1111-111111111103',
            '11111111-1111-1111-1111-111111111104',
            # Business 2 Users
            '22222222-2222-2222-2222-222222222201',
            '22222222-2222-2222-2222-222222222202',
            '22222222-2222-2222-2222-222222222203',
            '22222222-2222-2222-2222-222222222204',
            # Business 3 Users
            '33333333-3333-3333-3333-333333333301',
            '33333333-3333-3333-3333-333333333302',
            '33333333-3333-3333-3333-333333333303',
            '33333333-3333-3333-3333-333333333304'
        ]
        
        # Delete in correct order (children first, then parents) to prevent foreign key violations
        print("Deleting business impact links...")
        deleted_impact_links = session.query(BusinessImpactLink).filter(
            BusinessImpactLink.business_id.in_(business_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_impact_links} impact links")
        
        print("Deleting business shops...")
        deleted_shops = session.query(BusinessShop).filter(
            BusinessShop.business_id.in_(business_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_shops} business shops")
        
        print("Deleting business cause preferences...")
        deleted_cause_prefs = session.query(BusinessCausePreference).filter(
            BusinessCausePreference.business_id.in_(business_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_cause_prefs} cause preferences")
        
        print("Deleting business social media...")
        deleted_social_media = session.query(BusinessSocialMedia).filter(
            BusinessSocialMedia.business_id.in_(business_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_social_media} social media profiles")
        
        print("Deleting business users...")
        deleted_business_users = session.query(BusinessUser).filter(
            BusinessUser.business_id.in_(business_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_business_users} business user relationships")
        
        print("Deleting businesses...")
        deleted_businesses = session.query(Business).filter(
            Business.business_id.in_(business_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_businesses} businesses")
        
        print("Deleting app users...")
        deleted_app_users = session.query(AppUser).filter(
            AppUser.app_user_id.in_(app_user_ids)
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_app_users} app users")
        
        # Commit all deletions
        session.commit()
        session.close()
        
        total_deleted = (deleted_impact_links + deleted_shops + deleted_cause_prefs + 
                        deleted_social_media + deleted_business_users + deleted_businesses + deleted_app_users)
        
        print(f"\nSpecific seed data deleted successfully!")
        print(f"Total records deleted: {total_deleted}")
        print("\nDeleted specific test data:")
        print("- 3 test businesses (Eco Solutions, Tech Innovations, Local Harvest)")
        print("- 12 test app users")
        print("- All related business relationships and preferences")
        print("\nAll other data preserved (reference data + any other businesses/users)")
        
    except Exception as e:
        print(f"Error deleting seed data: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise

if __name__ == "__main__":
    delete_seed_data()