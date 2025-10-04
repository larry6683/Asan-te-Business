"""
Main database setup script that creates tables and populates data.
This replaces the entire SQL migration process with SQLAlchemy.
"""

import sys
import os
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
print(f"Adding to Python path: {project_root}")
sys.path.insert(0, project_root)

# Try to import the tables directly from src
try:
    from src.public.tables import (
        Base, UserType, BusinessSize, BusinessUserPermissionRole,
        BeneficiarySize, BeneficiaryUserPermissionRole, CauseCategory, 
        Cause, CausePreferenceRank, RegistrationType, SocialMediaType, 
        ShopType
    )
    print("✅ Successfully imported table models")
except ImportError as e:
    print(f"❌ Failed to import table models: {e}")
    print("Let's check what's available...")
    
    # Check src directory
    src_path = os.path.join(project_root, 'src')
    if os.path.exists(src_path):
        print(f"✅ src directory exists at: {src_path}")
        print("Contents:")
        for item in os.listdir(src_path):
            print(f"  {item}")
            
        # Check public directory
        public_path = os.path.join(src_path, 'public')
        if os.path.exists(public_path):
            print(f"✅ public directory exists")
            print("Public contents:")
            for item in os.listdir(public_path):
                print(f"  {item}")
                
            # Check tables directory  
            tables_path = os.path.join(public_path, 'tables')
            if os.path.exists(tables_path):
                print(f"✅ tables directory exists")
                print("Tables contents:")
                for item in os.listdir(tables_path):
                    print(f"  {item}")
                    
                # Check if __init__.py exists in tables
                init_file = os.path.join(tables_path, '__init__.py')
                if os.path.exists(init_file):
                    print("✅ __init__.py exists in tables")
                    with open(init_file, 'r') as f:
                        content = f.read()
                        print("__init__.py content preview:")
                        print(content[:500] + "..." if len(content) > 500 else content)
                else:
                    print("❌ __init__.py missing in tables")
    
    print("\nTrying alternative import approach...")
    
    # Try absolute imports
    try:
        import src.public.tables as tables_module
        Base = tables_module.Base
        UserType = tables_module.UserType
        BusinessSize = tables_module.BusinessSize
        BusinessUserPermissionRole = tables_module.BusinessUserPermissionRole
        BeneficiarySize = tables_module.BeneficiarySize
        BeneficiaryUserPermissionRole = tables_module.BeneficiaryUserPermissionRole
        CauseCategory = tables_module.CauseCategory
        Cause = tables_module.Cause
        CausePreferenceRank = tables_module.CausePreferenceRank
        RegistrationType = tables_module.RegistrationType
        SocialMediaType = tables_module.SocialMediaType
        ShopType = tables_module.ShopType
        print("✅ Successfully imported via alternative method")
    except ImportError as e2:
        print(f"❌ Alternative import also failed: {e2}")
        print("Please check that:")
        print("1. All Python files in src/public/tables/ have proper syntax")
        print("2. __init__.py exists and imports all models")
        print("3. All dependencies are installed (pip install -r requirements.txt)")
        sys.exit(1)

# Try to import seed data function
try:
    from scripts.seed_data.public_seed_data import create_seed_data
    print("✅ Successfully imported seed data function")
except ImportError as e:
    print(f"⚠️  Could not import seed data function: {e}")
    print("Will skip seed data creation")
    
    def create_seed_data(database_url):
        print("Seed data creation skipped - import not available")
        pass

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
    """Populate user_type table"""
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
    """Populate business_size table"""
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
    """Populate cause_category and cause tables"""
    print("Populating cause categories and causes...")
    
    # Create cause categories
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
    
    # Create causes
    causes = [
        # Community Causes
        Cause(code=1, cause_name='Homelessness', cause_category_id=community_id),
        Cause(code=2, cause_name='Events & Advocacy', cause_category_id=community_id),
        Cause(code=3, cause_name='First Responders', cause_category_id=community_id),
        Cause(code=4, cause_name='Disadvantaged Populations', cause_category_id=community_id),
        Cause(code=5, cause_name='Schools & Teachers', cause_category_id=community_id),
        Cause(code=6, cause_name='Animal Welfare', cause_category_id=community_id),
        
        # Social Causes
        Cause(code=7, cause_name='Sports', cause_category_id=social_id),
        Cause(code=8, cause_name='Arts', cause_category_id=social_id),
        Cause(code=9, cause_name='Faith Based Orgs', cause_category_id=social_id),
        Cause(code=10, cause_name='Education', cause_category_id=social_id),
        Cause(code=11, cause_name='Social Justice', cause_category_id=social_id),
        Cause(code=12, cause_name='Health & Wellbeing', cause_category_id=social_id),
        
        # Entrepreneurship Causes
        Cause(code=13, cause_name='Youth Empowerment', cause_category_id=entrepreneurship_id),
        Cause(code=14, cause_name='Innovation', cause_category_id=entrepreneurship_id),
        Cause(code=15, cause_name='Sustainable Innovation', cause_category_id=entrepreneurship_id),
        Cause(code=16, cause_name='Social Entrepreneurship', cause_category_id=entrepreneurship_id),
        
        # Environment Causes
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
    """Populate all reference/lookup tables with initial data"""
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
    """Complete database setup"""
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
            print(f"Warning: Could not create seed data: {e}")
            print("Database setup will continue without seed data")
    
    print("\nDatabase setup completed successfully!")
    print("\nWhat was created:")
    print("• All SQLAlchemy tables")
    print("• Reference data (user types, business sizes, causes, etc.)")
    if include_seed_data:
        print("• Test seed data (attempted)")
    
    return True

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
        print("Verification not implemented yet")
        return 0
    else:
        include_seed = not args.no_seed
        success = setup_database_full(database_url, include_seed_data=include_seed)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())