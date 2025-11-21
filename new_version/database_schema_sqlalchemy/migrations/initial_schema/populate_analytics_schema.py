"""
Analytics Schema Setup Script

Creates the analytics schema and populates the registration_step table
with the 6 predefined steps from the CU Boulder specification.

Usage:
    python populate_analytics.py
"""

# NEW (works with your project structure)
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker


# Add project root to path
project_root = Path(__file__).parent.parent.parent  # Goes up to database_schema_sqlalchemy
sys.path.insert(0, str(project_root))

from src.analytics.tables import Base as AnalyticsBase, RegistrationStep, REGISTRATION_STEPS, RegistrationInteraction
from src.public.tables import AppUser  


def create_database_url(host="localhost", port="5432", user="asante_dev", password="password", database="postgres"):
    """Create database connection URL"""
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def create_analytics_schema(engine):
    """Create the analytics schema if it doesn't exist"""
    print("Creating analytics schema...")
    try:
        with engine.connect() as conn:
            # Create schema
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics"))
            conn.commit()
            print("✅ Analytics schema created")
    except Exception as e:
        print(f"Error creating schema: {e}")
        raise


def drop_analytics_tables(engine):
    """Drop existing analytics tables (for clean setup)"""
    print("Dropping existing analytics tables...")
    try:
        with engine.connect() as conn:
            # Drop tables in correct order (interaction first due to FK)
            conn.execute(text("DROP TABLE IF EXISTS analytics.registration_interaction CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS analytics.registration_step CASCADE"))
            conn.commit()
            print("✅ Existing tables dropped")
    except Exception as e:
        print(f"⚠️  Warning: Could not drop tables: {e}")


def create_analytics_tables(engine):
    """Create analytics tables using SQLAlchemy models"""
    print("Creating analytics tables...")
    print("Creating analytics tables...")
    try:
        # Force AppUser to be in metadata by accessing it
        _ = AppUser.__table__
        
        # Now create tables
        AnalyticsBase.metadata.create_all(engine)
        print("✅ Analytics tables created")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'analytics' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"\nCreated {len(tables)} tables in analytics schema:")
            for table in tables:
                print(f"  - analytics.{table}")
                
    except Exception as e:
        print(f"Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        raise


def populate_registration_steps(engine):
    """Populate the registration_step table with predefined steps"""
    print("\nPopulating registration steps...")
    
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        for step_data in REGISTRATION_STEPS:
            # Check if step already exists
            existing = session.query(RegistrationStep).filter_by(code=step_data['code']).first()
            
            if existing:
                print(f"  - Updating step {step_data['code']}: {step_data['step_name']}")
                existing.step_name = step_data['step_name']
                existing.step_order = step_data['step_order']
                existing.description = step_data['description']
            else:
                print(f"  - Creating step {step_data['code']}: {step_data['step_name']}")
                step = RegistrationStep(**step_data)
                session.add(step)
        
        session.commit()
        
        # Verify
        count = session.query(RegistrationStep).count()
        print(f"\n✅ Registration steps populated: {count} steps")
        
        # Display all steps
        steps = session.query(RegistrationStep).order_by(RegistrationStep.step_order).all()
        print("\nRegistration steps in order:")
        for step in steps:
            print(f"  {step.step_order}. {step.step_name} (code: {step.code})")
            print(f"     {step.description[:80]}...")
        
        session.close()
        
    except Exception as e:
        print(f"Error populating registration steps: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise


def verify_indexes(engine):
    """Verify that all required indexes were created"""
    print("\nVerifying indexes...")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    tablename,
                    indexname
                FROM pg_indexes
                WHERE schemaname = 'analytics'
                ORDER BY tablename, indexname
            """))
            
            indexes = result.fetchall()
            print(f"Found {len(indexes)} indexes:")
            for table, index in indexes:
                print(f"  - {table}: {index}")
                
    except Exception as e:
        print(f"⚠️  Warning: Could not verify indexes: {e}")


def setup_analytics_schema(database_url="postgresql://asante_dev:password@localhost:5432/postgres", clean_start=True):
    """Complete analytics schema setup"""
    print("="*60)
    print("ANALYTICS SCHEMA SETUP")
    print("="*60)
    print(f"\nDatabase: {database_url}\n")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL")
        
        # Create schema
        create_analytics_schema(engine)
        
        # Optionally drop existing tables for clean start
        if clean_start:
            drop_analytics_tables(engine)
        
        # Create tables
        create_analytics_tables(engine)
        
        # Populate registration steps
        populate_registration_steps(engine)
        
        # Verify indexes
        verify_indexes(engine)
        
        print("\n" + "="*60)
        print("✅ ANALYTICS SCHEMA SETUP COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Run analytics_seed_data.py to populate test interaction data")
        print("2. Test queries against the analytics schema")
        print("3. Connect the API to track registration steps")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup analytics schema and tables')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='5432', help='Database port')
    parser.add_argument('--user', default='asante_dev', help='Database user')
    parser.add_argument('--password', default='password', help='Database password')
    parser.add_argument('--database', default='postgres', help='Database name')
    parser.add_argument('--no-clean', action='store_true', help='Keep existing data')
    
    args = parser.parse_args()
    
    database_url = create_database_url(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )
    
    clean_start = not args.no_clean
    success = setup_analytics_schema(database_url, clean_start=clean_start)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())