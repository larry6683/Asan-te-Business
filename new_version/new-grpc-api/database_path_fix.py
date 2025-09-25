# new_version/new-grpc-api/src/database_path_fix.py
"""
Simple module to fix Python path for SQLAlchemy imports
Import this at the top of any file that needs SQLAlchemy models
"""

import sys
import os

def setup_sqlalchemy_path():
    """Add the database schema path to Python path"""
    
    # Get the current file's directory
    current_file = os.path.abspath(__file__)
    print(f"Current file: {current_file}")
    
    # Navigate to the database schema directory
    # From: new-grpc-api/src/database_path_fix.py
    # To:   new_version/database_schema_sqlalchemy/
    current_dir = os.path.dirname(current_file)  # src/
    project_root = os.path.dirname(current_dir)  # new-grpc-api/
    parent_dir = os.path.dirname(project_root)    # new_version/
    
    print(f"Project structure:")
    print(f"  current_dir: {current_dir}")
    print(f"  project_root: {project_root}")  
    print(f"  parent_dir: {parent_dir}")
    
    # Try multiple possible locations for the database schema
    possible_paths = [
        # Most likely location based on your structure
        os.path.join(parent_dir, 'database_schema_sqlalchemy'),
        
        # Alternative locations
        os.path.join(project_root, '..', 'database_schema_sqlalchemy'),
        os.path.join(parent_dir, '..', 'database_schema_sqlalchemy'),
        
        # In case it's directly in the parent
        os.path.join(project_root, 'database_schema_sqlalchemy'),
        
        # Windows-specific path variations
        os.path.join(parent_dir, 'database-schema-sqlalchemy'),
        
        # Absolute path fallback based on your error message
        r'C:\Users\battu\Downloads\Asan-te-Business\new_version\database_schema_sqlalchemy'
    ]
    
    for db_schema_path in possible_paths:
        abs_path = os.path.abspath(db_schema_path)
        print(f"Checking path: {abs_path}")
        
        if os.path.exists(abs_path):
            # Check if it contains the expected database_layer directory
            database_layer_path = os.path.join(abs_path, 'database_layer')
            if os.path.exists(database_layer_path):
                if abs_path not in sys.path:
                    sys.path.insert(0, abs_path)
                    print(f"✅ Added SQLAlchemy path: {abs_path}")
                return True
            else:
                print(f"   - Path exists but no database_layer subdirectory found")
        else:
            print(f"   - Path does not exist")
    
    print(f"❌ Could not find database schema directory")
    print(f"Please check that the database_schema_sqlalchemy directory exists")
    
    # List what's actually in the parent directory
    try:
        parent_contents = os.listdir(parent_dir)
        print(f"Contents of {parent_dir}:")
        for item in parent_contents:
            item_path = os.path.join(parent_dir, item)
            item_type = "DIR" if os.path.isdir(item_path) else "FILE"
            print(f"  {item_type}: {item}")
    except Exception as e:
        print(f"Could not list parent directory: {e}")
    
    return False

def import_sqlalchemy_models():
    """Import SQLAlchemy models with proper error handling"""
    if not setup_sqlalchemy_path():
        return None, None, False
    
    try:
        from database_layer.models import AppUser, UserType
        print("✅ SQLAlchemy models imported successfully")
        return AppUser, UserType, True
    except ImportError as e:
        print(f"❌ Failed to import SQLAlchemy models: {e}")
        return None, None, False

# Auto-setup when this module is imported
print("🔍 Setting up SQLAlchemy path...")
SQLALCHEMY_AVAILABLE = setup_sqlalchemy_path()

if __name__ == "__main__":
    print("Testing SQLAlchemy path setup...")
    AppUser, UserType, available = import_sqlalchemy_models()
    if available:
        print("✅ SQLAlchemy models available")
    else:
        print("❌ SQLAlchemy models not available")
        print("")
        print("💡 To fix this:")
        print("1. Make sure the database_schema_sqlalchemy directory exists")
        print("2. It should be at: new_version/database_schema_sqlalchemy/")
        print("3. It should contain a database_layer/ subdirectory")
        print("4. Run this to verify:")
        print("   cd ../database_schema_sqlalchemy")
        print("   ls -la database_layer/")