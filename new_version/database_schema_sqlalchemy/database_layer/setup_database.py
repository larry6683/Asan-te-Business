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

from database_layer.models import Base
from database_layer.scripts.populate_reference_data import populate_all_reference_data
from database_layer.scripts.create_seed_data import create_seed_data

def create_database_url(host="localhost", port="5432", user="asante_dev", password="password", database="postgres"):
    """Create database connection URL"""
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

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
        print("\n Populating reference data...")
        populate_all_reference_data(database_url)
    except Exception as e:
        print(f"Error populating reference data: {e}")
        return False
    
    # Create seed data if requested
    if include_seed_data:
        try:
            print("\n Creating seed data...")
            create_seed_data(database_url)
        except Exception as e:
            print(f"Error creating seed data: {e}")
            return False
    
    print("\n Database setup completed successfully!")
    print("\n What was created:")
    print(" All SQLAlchemy tables")
    print(" Reference data (user types, business sizes, causes, etc.)")
    if include_seed_data:
        print(" Test seed data (3 businesses with users)")

    
    return True

def verify_data(database_url):
    """Verify that data was created correctly"""
    print("\n Verifying database data...")
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Quick verification of core tables
        from database_layer.models import (
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