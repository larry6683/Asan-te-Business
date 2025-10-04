import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env from project root
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)
    print(f"✓ Loaded environment from: {env_path}")
except ImportError:
    print("Warning: python-dotenv not installed, using environment variables only")

# Add database schema to path
current_dir = os.path.dirname(os.path.abspath(__file__))
grpc_api_dir = os.path.dirname(os.path.dirname(current_dir))
new_version_dir = os.path.dirname(grpc_api_dir)
db_schema_path = os.path.join(new_version_dir, 'database_schema_sqlalchemy')

if os.path.exists(db_schema_path):
    if db_schema_path not in sys.path:
        sys.path.insert(0, db_schema_path)
    print(f"✓ Added database path: {db_schema_path}")
else:
    print(f"✗ Warning: Database path not found: {db_schema_path}")

class Config:
    # Database configuration from environment variables
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'asante_production')
    DB_USER = os.getenv('DB_USER', 'asante_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'SecurePass123!')
    
    @classmethod
    def get_database_url(cls):
        url = f'postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'
        return url
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without password)"""
        print("=" * 50)
        print("Database Configuration:")
        print(f"  Host: {cls.DB_HOST}")
        print(f"  Port: {cls.DB_PORT}")
        print(f"  Database: {cls.DB_NAME}")
        print(f"  User: {cls.DB_USER}")
        print(f"  Password: {'*' * len(cls.DB_PASSWORD)}")
        print("=" * 50)
