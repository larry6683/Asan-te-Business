"""
Main database setup script that creates tables and populates data.
This replaces the entire SQL migration process with SQLAlchemy.
"""

import sys
import os
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path to import database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from database_layer.src.public.tables import (
    Base, UserType, BusinessSize, BusinessUserPermissionRole,
    BeneficiarySize, BeneficiaryUserPermissionRole, CauseCategory, 
    Cause, CausePreferenceRank, RegistrationType, SocialMediaType, 
    ShopType
)
from database_layer.scripts.seed_data.public_seed_data import create_seed_data

def create_database_url(host="localhost", port="5432", user="asante_dev", password="password", database="postgres"):
    """Create database connection URL"""
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def create_session(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """Create database session"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return engine, Session()

def test_connection(database_url):
    """Test database connection"""
    print("Testing database connection...")
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"Connected to PostgreSQL: {version[:50]}...")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def check_extensions(database_url):
    """Check and install required PostgreSQL extensions"""
    print("Checking PostgreSQL extensions...")
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Check if pgcrypto exists
            result = conn.execute(text("SELECT COUNT(*) FROM pg_extension WHERE extname = 'pgcrypto'"))
            pgcrypto_installed = result.fetchone()[0] > 0
            
            if not pgcrypto_installed:
                print("Installing pgcrypto extension...")
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
                conn.commit()
                print("pgcrypto extension installed")
            else:
                print("pgcrypto extension already installed")
                
    except Exception as e:
        print(f"⚠️  Warning: Could not check/install extensions: {e}")
        print("You may need to install pgcrypto manually in pgAdmin:")
        print("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

def create_tables(database_url):
    """Create all tables using SQLAlchemy models"""
    print("Creating database tables...")
    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(engine)
        print("All tables created successfully")
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
        
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def populate_user_types(session):
    """Populate user_type table - equivalent to populate_user_type_data.sql"""
    print("Populating user types...")
    
    user_types = [
        UserType(code=1, user_type_name='business user'),
        UserType(code=2, user_type_name='beneficiary user'), 
        UserType(code=3, user_type_name='consumer user')
    ]
    
    for user_type in user_types:
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
    """Populate cause_category and cause tables with updated UI structure"""
    print("Populating cause categories and causes...")
    
    # Create cause categories with new structure
    cause_categories = [
        CauseCategory(code=1, cause_category_name='Community'),
        CauseCategory(code=2, cause_category_name='Social'),
        CauseCategory(code=3, cause_category_name='Entrepreneurship'),
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
    entrepreneurship_id = session.query(CauseCategory).filter_by(code=3).first().cause_category_id
    environment_id = session.query(CauseCategory).filter_by(code=4).first().cause_category_id
    emergency_id = session.query(CauseCategory).filter_by(code=5).first().cause_category_id
    
    # Create causes with new structure
    causes = [
        # Community Causes (6 causes)
        Cause(code=1, cause_name='Homelessness', cause_category_id=community_id),
        Cause(code=2, cause_name='Events & Advocacy', cause_category_id=community_id),
        Cause(code=3, cause_name='First Responders', cause_category_id=community_id),
        Cause(code=4, cause_name='Disadvantaged Populations', cause_category_id=community_id),
        Cause(code=5, cause_name='Schools & Teachers', cause_category_id=community_id),
        Cause(code=6, cause_name='Animal Welfare', cause_category_id=community_id),
        
        # Social Causes (7 causes)
        Cause(code=7, cause_name='Sports', cause_category_id=social_id),
        Cause(code=8, cause_name='Arts', cause_category_id=social_id),
        Cause(code=9, cause_name='Faith Based Orgs', cause_category_id=social_id),
        Cause(code=10, cause_name='Education', cause_category_id=social_id),
        Cause(code=11, cause_name='Social Justice', cause_category_id=social_id),
        Cause(code=12, cause_name='Health & Wellbeing', cause_category_id=social_id),
        
        # Entrepreneurship Causes (4 causes) 
        Cause(code=13, cause_name='Youth Empowerment', cause_category_id=entrepreneurship_id),
        Cause(code=14, cause_name='Innovation', cause_category_id=entrepreneurship_id),
        Cause(code=15, cause_name='Sustainable Innovation', cause_category_id=entrepreneurship_id),
        Cause(code=16, cause_name='Social Entrepreneurship', cause_category_id=entrepreneurship_id),
        
        # Environment Causes (5 causes)
        Cause(code=17, cause_name='Droughts & Fire Management', cause_category_id=environment_id),
        Cause(code=18, cause_name='Climate Advocacy', cause_category_id=environment_id),
        Cause(code=19, cause_name='Water Sustainability', cause_category_id=environment_id),
        Cause(code=20, cause_name='Food Systems', cause_category_id=environment_id),
        Cause(code=21, cause_name='Wildlife Protection', cause_category_id=environment_id),
        
        # Emergency Relief Causes
        Cause(code=22, cause_name='Emergency Relief', cause_category_id=emergency_id)
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
        print("\nAll reference data populated successfully!")
        
    except Exception as e:
        print(f"Error populating reference data: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise

def setup_database_full(database_url, include_seed_data=True):
    """
    Complete database setup: create tables, populate reference data, and optionally seed data
    """
    print("Starting full database setup...")
    print(f"Database URL: {database_url}")
    
    # Test connection
    if not test_connection(database_url):
        return False
    
    # Check extensions
    check_extensions(database_url)
    
    # Create tables
    if not create_tables(database_url):
        return False
    
    # Populate reference data
    try:
        print("\nPopulating reference data...")
        populate_all_reference_data(database_url)
    except Exception as e:
        print(f"Error populating reference data: {e}")
        return False
    
    # Create seed data if requested
    if include_seed_data:
        try:
            print("\nCreating seed data...")
            create_seed_data(database_url)
        except Exception as e:
            print(f"Error creating seed data: {e}")
            return False
    
    print("\nDatabase setup completed successfully!")
    print("\nWhat was created:")
    print("• All SQLAlchemy tables")
    print("• Reference data (user types, business sizes, causes, etc.)")
    if include_seed_data:
        print("• Test seed data (3 businesses with users)")
    
    return True

def verify_data(database_url):
    """Verify that data was created correctly"""
    print("\nVerifying database data...")
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Quick verification of core tables
        from database_layer.src.public.tables import (
            UserType, BusinessSize, Business, AppUser, 
            BusinessUser, Cause, CauseCategory
        )
        
        # Check reference data counts
        user_type_count = session.query(UserType).count()
        business_size_count = session.query(BusinessSize).count()
        cause_count = session.query(Cause).count()
        cause_category_count = session.query(CauseCategory).count()
        
        print(f"Reference data:")
        print(f"  - User types: {user_type_count}")
        print(f"  - Business sizes: {business_size_count}")
        print(f"  - Cause categories: {cause_category_count}")
        print(f"  - Causes: {cause_count}")
        
        # Check seed data counts
        business_count = session.query(Business).count()
        app_user_count = session.query(AppUser).count()
        business_user_count = session.query(BusinessUser).count()
        
        print(f"Seed data:")
        print(f"  - Businesses: {business_count}")
        print(f"  - App users: {app_user_count}")
        print(f"  - Business users: {business_user_count}")
        
        # Test a query
        eco_business = session.query(Business).filter_by(business_name='Eco Solutions Inc.').first()
        if eco_business:
            print(f"Sample business found: {eco_business.business_name}")
            print(f"   Location: {eco_business.location_city}, {eco_business.location_state}")
        
        session.close()
        print("Data verification successful")
        return True
        
    except Exception as e:
        print(f"Data verification failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Setup Asante database using SQLAlchemy')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='5432', help='Database port')
    parser.add_argument('--user', default='asante_dev', help='Database user')
    parser.add_argument('--password', default='password', help='Database password')
    parser.add_argument('--database', default='postgres', help='Database name')
    parser.add_argument('--no-seed', action='store_true', help='Skip creating seed data')
    parser.add_argument('--verify-only', action='store_true', help='Only verify existing data')
    
    args = parser.parse_args()
    
    database_url = create_database_url(
        host=args.host, 
        port=args.port, 
        user=args.user, 
        password=args.password, 
        database=args.database
    )
    
    if args.verify_only:
        success = verify_data(database_url)
    else:
        include_seed = not args.no_seed
        success = setup_database_full(database_url, include_seed_data=include_seed)
        
        if success:
            verify_data(database_url)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()