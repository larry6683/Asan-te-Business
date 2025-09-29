import os
import sys

# Add database schema to path
current_dir = os.path.dirname(os.path.abspath(__file__))
grpc_api_dir = os.path.dirname(os.path.dirname(current_dir))
new_version_dir = os.path.dirname(grpc_api_dir)
db_schema_path = os.path.join(new_version_dir, 'database_schema_sqlalchemy')

if os.path.exists(db_schema_path):
    if db_schema_path not in sys.path:
        sys.path.insert(0, db_schema_path)
    print(f"Added database path: {db_schema_path}")
else:
    print(f"Warning: Database path not found: {db_schema_path}")

class Config:
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'asante_dev')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    
    @classmethod
    def get_database_url(cls):
        return f'postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'
