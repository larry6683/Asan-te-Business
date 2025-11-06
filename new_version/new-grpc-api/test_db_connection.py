#!/usr/bin/env python3
"""
Test database connection with new credentials
"""
import sys
sys.path.insert(0, 'src')

from config.config import Config
from sqlalchemy import create_engine, text

def test_connection():
    print("\n" + "=" * 50)
    print("Testing Database Connection")
    print("=" * 50 + "\n")
    
    # Print configuration
    Config.print_config()
    
    try:
        # Create engine
        database_url = Config.get_database_url()
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"\n✓ Connected successfully!")
            print(f"\nPostgreSQL Version:")
            print(f"  {version[:80]}...")
            
            # Count tables
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.fetchone()[0]
            print(f"\n✓ Found {table_count} tables in database")
            
            # Test a simple query on user_type table
            result = conn.execute(text("SELECT COUNT(*) FROM user_type"))
            user_type_count = result.fetchone()[0]
            print(f"✓ user_type table has {user_type_count} records")
            
            return True
            
    except Exception as e:
        print(f"\n✗ Connection failed!")
        print(f"  Error: {e}")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
