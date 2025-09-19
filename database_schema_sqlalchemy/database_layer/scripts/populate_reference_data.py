"""
Convert SQL populate scripts to Python using SQLAlchemy models.
This replaces all the populate_*.sql files with Python equivalents.

Also replaces the save_*.sql stored procedures with Python upsert logic:
- save_user_type.sql → populate_user_types() function with upsert
- save_business_size.sql → populate_business_sizes() function with upsert
- save_cause_category.sql → populate_cause_categories_and_causes() function with upsert
- etc.

The upsert logic (insert or update if exists) is handled by checking for existing
records by code and updating if found, or inserting if new.
"""

import sys
import os

# Add the project root to Python path to import database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_layer.models import (
    Base, UserType, BusinessSize, BusinessUserPermissionRole,
    BeneficiarySize, BeneficiaryUserPermissionRole, CauseCategory, 
    Cause, CausePreferenceRank, RegistrationType, SocialMediaType, 
    ShopType
)

def create_session(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """Create database session"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return engine, Session()

def populate_user_types(session):
    """Populate user_type table - equivalent to populate_user_type_data.sql"""
    print("Populating user types...")
    
    user_types = [
        UserType(code=1, user_type_name='business user'),
        UserType(code=2, user_type_name='beneficiary user'), 
        UserType(code=3, user_type_name='consumer user')
    ]
    
    for user_type in user_types:
        # Use merge to handle duplicates (equivalent to ON CONFLICT DO UPDATE)
        existing = session.query(UserType).filter_by(code=user_type.code).first()
        if existing:
            existing.user_type_name = user_type.user_type_name
        else:
            session.add(user_type)
    
    session.commit()
    print("User types populated")

def populate_business_sizes(session):
    """Populate business_size table - equivalent to populate_business_size_data.sql"""
    print("Populating business sizes...")
    
    business_sizes = [
        BusinessSize(code=1, business_size_name='small'),
        BusinessSize(code=2, business_size_name='medium'),
        BusinessSize(code=3, business_size_name='large')
    ]
    
    for size in business_sizes:
        existing = session.query(BusinessSize).filter_by(code=size.code).first()
        if existing:
            existing.business_size_name = size.business_size_name
        else:
            session.add(size)
    
    session.commit()
    print("Business sizes populated")

def populate_business_user_permission_roles(session):
    """Populate business_user_permission_role table"""
    print("Populating business user permission roles...")
    
    roles = [
        BusinessUserPermissionRole(code=1, business_user_permission_role_name='Admin'),
        BusinessUserPermissionRole(code=2, business_user_permission_role_name='Team Member'),
        BusinessUserPermissionRole(code=3, business_user_permission_role_name='Removed')
    ]
    
    for role in roles:
        existing = session.query(BusinessUserPermissionRole).filter_by(code=role.code).first()
        if existing:
            existing.business_user_permission_role_name = role.business_user_permission_role_name
        else:
            session.add(role)
    
    session.commit()
    print("Business user permission roles populated")

def populate_beneficiary_sizes(session):
    """Populate beneficiary_size table"""
    print("Populating beneficiary sizes...")
    
    sizes = [
        BeneficiarySize(code=1, beneficiary_size_name='small'),
        BeneficiarySize(code=2, beneficiary_size_name='medium'),
        BeneficiarySize(code=3, beneficiary_size_name='large')
    ]
    
    for size in sizes:
        existing = session.query(BeneficiarySize).filter_by(code=size.code).first()
        if existing:
            existing.beneficiary_size_name = size.beneficiary_size_name
        else:
            session.add(size)
    
    session.commit()
    print("Beneficiary sizes populated")

def populate_beneficiary_user_permission_roles(session):
    """Populate beneficiary_user_permission_role table"""
    print("Populating beneficiary user permission roles...")
    
    roles = [
        BeneficiaryUserPermissionRole(code=1, beneficiary_user_permission_role_name='Admin'),
        BeneficiaryUserPermissionRole(code=2, beneficiary_user_permission_role_name='Team Member'),
        BeneficiaryUserPermissionRole(code=3, beneficiary_user_permission_role_name='Removed')
    ]
    
    for role in roles:
        existing = session.query(BeneficiaryUserPermissionRole).filter_by(code=role.code).first()
        if existing:
            existing.beneficiary_user_permission_role_name = role.beneficiary_user_permission_role_name
        else:
            session.add(role)
    
    session.commit()
    print("Beneficiary user permission roles populated")

def populate_cause_categories_and_causes(session):
    """Populate cause_category and cause tables - equivalent to populate_cause_and_cause_category_data.sql"""
    print("Populating cause categories and causes...")
    
    # First create cause categories
    cause_categories = [
        CauseCategory(code=1, cause_category_name='Community'),
        CauseCategory(code=2, cause_category_name='Social'),
        CauseCategory(code=3, cause_category_name='Innovation'),
        CauseCategory(code=4, cause_category_name='Environment'),
        CauseCategory(code=5, cause_category_name='Emergency Relief')
    ]
    
    for category in cause_categories:
        existing = session.query(CauseCategory).filter_by(code=category.code).first()
        if existing:
            existing.cause_category_name = category.cause_category_name
        else:
            session.add(category)
    
    session.commit()
    
    # Get category IDs for foreign keys
    community_id = session.query(CauseCategory).filter_by(code=1).first().cause_category_id
    social_id = session.query(CauseCategory).filter_by(code=2).first().cause_category_id
    innovation_id = session.query(CauseCategory).filter_by(code=3).first().cause_category_id
    environment_id = session.query(CauseCategory).filter_by(code=4).first().cause_category_id
    emergency_id = session.query(CauseCategory).filter_by(code=5).first().cause_category_id
    
    # Create causes
    causes = [
        # Community Causes
        Cause(code=1, cause_name='Homelessness', cause_category_id=community_id),
        Cause(code=2, cause_name='Events & Advocacy', cause_category_id=community_id),
        Cause(code=3, cause_name='First Responders', cause_category_id=community_id),
        Cause(code=4, cause_name='Disadvantaged Populations', cause_category_id=community_id),
        Cause(code=5, cause_name='Schools & Teachers', cause_category_id=community_id),
        
        # Social Causes
        Cause(code=6, cause_name='Sports', cause_category_id=social_id),
        Cause(code=7, cause_name='Arts', cause_category_id=social_id),
        Cause(code=8, cause_name='Education', cause_category_id=social_id),
        Cause(code=9, cause_name='Social Justice', cause_category_id=social_id),
        Cause(code=10, cause_name='Mental Health & Wellbeing', cause_category_id=social_id),
        
        # Innovation Causes
        Cause(code=11, cause_name='Youth Empowerment', cause_category_id=innovation_id),
        Cause(code=12, cause_name='Social Innovation', cause_category_id=innovation_id),
        Cause(code=13, cause_name='Sustainable Innovation', cause_category_id=innovation_id),
        Cause(code=14, cause_name='Social Entrepreneurship', cause_category_id=innovation_id),
        
        # Environment Causes
        Cause(code=15, cause_name='Drought & Fire Management', cause_category_id=environment_id),
        Cause(code=16, cause_name='Climate Advocacy', cause_category_id=environment_id),
        Cause(code=17, cause_name='Climate Refugees', cause_category_id=environment_id),
        Cause(code=18, cause_name='Water Sustainability', cause_category_id=environment_id),
        
        # Emergency Relief Causes
        Cause(code=19, cause_name='Emergency Relief', cause_category_id=emergency_id)
    ]
    
    for cause in causes:
        existing = session.query(Cause).filter_by(code=cause.code).first()
        if existing:
            existing.cause_name = cause.cause_name
            existing.cause_category_id = cause.cause_category_id
        else:
            session.add(cause)
    
    session.commit()
    print("Cause categories and causes populated")

def populate_cause_preference_ranks(session):
    """Populate cause_preference_rank table"""
    print("Populating cause preference ranks...")
    
    ranks = [
        CausePreferenceRank(code=1, cause_preference_rank_name='unranked'),
        CausePreferenceRank(code=2, cause_preference_rank_name='primary'),
        CausePreferenceRank(code=3, cause_preference_rank_name='supporting')
    ]
    
    for rank in ranks:
        existing = session.query(CausePreferenceRank).filter_by(code=rank.code).first()
        if existing:
            existing.cause_preference_rank_name = rank.cause_preference_rank_name
        else:
            session.add(rank)
    
    session.commit()
    print("Cause preference ranks populated")

def populate_registration_types(session):
    """Populate registration_type table"""
    print("Populating registration types...")
    
    types = [
        RegistrationType(code=1, registration_type_name='business'),
        RegistrationType(code=2, registration_type_name='non-profit'),
        RegistrationType(code=3, registration_type_name='consumer')
    ]
    
    for reg_type in types:
        existing = session.query(RegistrationType).filter_by(code=reg_type.code).first()
        if existing:
            existing.registration_type_name = reg_type.registration_type_name
        else:
            session.add(reg_type)
    
    session.commit()
    print("Registration types populated")

def populate_social_media_types(session):
    """Populate social_media_type table"""
    print("Populating social media types...")
    
    types = [
        SocialMediaType(code=0, social_media_type_name='unspecified'),
        SocialMediaType(code=1, social_media_type_name='linkedin'),
        SocialMediaType(code=2, social_media_type_name='instagram'),
        SocialMediaType(code=3, social_media_type_name='facebook')
    ]
    
    for media_type in types:
        existing = session.query(SocialMediaType).filter_by(code=media_type.code).first()
        if existing:
            existing.social_media_type_name = media_type.social_media_type_name
        else:
            session.add(media_type)
    
    session.commit()
    print("Social media types populated")

def populate_shop_types(session):
    """Populate shop_type table"""
    print("Populating shop types...")
    
    types = [
        ShopType(code=1, shop_type_name='shopify')
    ]
    
    for shop_type in types:
        existing = session.query(ShopType).filter_by(code=shop_type.code).first()
        if existing:
            existing.shop_type_name = shop_type.shop_type_name
        else:
            session.add(shop_type)
    
    session.commit()
    print("Shop types populated")

def populate_all_reference_data(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """
    Populate all reference/lookup tables with initial data.
    This replaces all the populate_*.sql scripts.
    """
    print("🚀 Starting reference data population...")
    
    try:
        engine, session = create_session(database_url)
        
        # Populate in dependency order
        populate_user_types(session)
        populate_business_sizes(session)
        populate_business_user_permission_roles(session)
        populate_beneficiary_sizes(session)
        populate_beneficiary_user_permission_roles(session)
        populate_cause_categories_and_causes(session) 
        populate_cause_preference_ranks(session)
        populate_registration_types(session)
        populate_social_media_types(session)
        populate_shop_types(session)
        
        session.close()
        print("\n All reference data populated successfully!")
        
    except Exception as e:
        print(f"Error populating reference data: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise

if __name__ == "__main__":
    populate_all_reference_data()