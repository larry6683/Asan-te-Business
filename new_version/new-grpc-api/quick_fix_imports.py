# new_version/new-grpc-api/quick_fix_imports.py
"""
Quick fix script to update import paths in existing files
"""

import os
import sys

def fix_file_imports():
    """Fix import statements in the handler files"""
    
    files_to_fix = [
        "src/features/user/get_user_by_email/get_user_by_email_query_handler.py",
        "src/features/user/create_user/create_user_command_handler.py",
        "src/converters/user_converter.py"
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Fixing imports in {file_path}")
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace problematic import
            old_import = "from database.sqlalchemy_models import AppUser, UserType"
            new_import_block = """# Add the database schema path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
db_schema_path = os.path.join(os.path.dirname(current_dir), 'database_schema_sqlalchemy')
if os.path.exists(db_schema_path):
    sys.path.insert(0, db_schema_path)

try:
    from database_layer.models import AppUser, UserType
    SQLALCHEMY_AVAILABLE = True
except ImportError as e:
    print(f"SQLAlchemy models not available: {e}")
    SQLALCHEMY_AVAILABLE = False
    AppUser = None
    UserType = None"""

            # Replace the import
            if old_import in content:
                # Add necessary imports at the top
                if "import sys" not in content:
                    content = "import sys\n" + content
                if "import os" not in content:
                    content = "import os\n" + content
                
                content = content.replace(old_import, new_import_block)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ Fixed {file_path}")
            else:
                print(f"⚠️  Import not found in {file_path}")
        else:
            print(f"❌ File not found: {file_path}")

def create_db_connection_file():
    """Create the database connection file"""
    
    db_connection_content = '''import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# Add the database schema path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_schema_path = os.path.join(os.path.dirname(current_dir), 'database_schema_sqlalchemy')
if os.path.exists(db_schema_path):
    sys.path.insert(0, db_schema_path)

try:
    from database_layer.models import Base
    from config.config import Config
    SQLALCHEMY_AVAILABLE = True
except ImportError as e:
    print(f"SQLAlchemy not available: {e}")
    SQLALCHEMY_AVAILABLE = False
    Base = None

class DatabaseConnection:
    _engine = None
    _SessionLocal = None
    
    @classmethod
    def initialize(cls):
        """Initialize database connection"""
        if not SQLALCHEMY_AVAILABLE:
            print("SQLAlchemy not available, using mock mode")
            return
            
        if cls._engine is None:
            try:
                # Get database config
                db_config = Config.get_database_config()
                
                # Create connection string
                database_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
                
                # Create engine
                cls._engine = create_engine(database_url)
                cls._SessionLocal = sessionmaker(bind=cls._engine)
                
                print(f"Database initialized: {db_config['host']}:{db_config['port']}/{db_config['dbname']}")
            except Exception as e:
                print(f"Database initialization failed: {e}")
                cls._engine = None
                cls._SessionLocal = None
    
    @classmethod
    @contextmanager
    def get_session(cls) -> Session:
        """Get database session with automatic cleanup"""
        if cls._SessionLocal is None:
            cls.initialize()
        
        if cls._SessionLocal is None:
            raise Exception("Database not available")
            
        session = cls._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_engine(cls):
        """Get database engine"""
        if cls._engine is None:
            cls.initialize()
        return cls._engine
'''
    
    # Create directory if it doesn't exist
    os.makedirs("src/database", exist_ok=True)
    
    # Write the file
    with open("src/database/db_connection.py", 'w', encoding='utf-8') as f:
        f.write(db_connection_content)
    
    print("✓ Created src/database/db_connection.py")

def create_local_config():
    """Create local config if it doesn't exist"""
    config_path = "src/config/local_config.py"
    
    if not os.path.exists(config_path):
        local_config_content = '''"""
Local configuration for gRPC API
"""
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "dbname": "postgres",
        "user": "asante_dev",
        "password": "password"
    },
    "logging": {
        "level": "DEBUG",
        "file": "app.log"
    },
    "datasource": "mock"  # Set to "db" to use SQLAlchemy, "mock" for testing
}
'''
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(local_config_content)
        
        print(f"✓ Created {config_path}")
    else:
        print(f"⚠️  {config_path} already exists")

if __name__ == "__main__":
    print("🔧 Quick fix for import issues...")
    
    # Check current directory
    if not os.path.exists("src"):
        print("❌ Please run this from the new-grpc-api directory")
        sys.exit(1)
    
    # Fix imports
    fix_file_imports()
    
    # Create database connection file
    create_db_connection_file()
    
    # Create local config
    create_local_config()
    
    print("✅ Quick fix completed!")
    print("")
    print("Next steps:")
    print("1. Make sure your database is running: docker ps | grep postgres")
    print("2. Update src/config/local_config.py with your database settings")
    print("3. Set datasource to 'db' in local_config.py to use SQLAlchemy")
    print("4. Run: chmod +x start_services_debug.sh")
    print("5. Run: ./start_services_debug.sh")