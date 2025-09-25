# new_version/new-grpc-api/check_directory_structure.py
"""
Check the directory structure to help debug the path issue
"""

import os
import sys

def check_structure():
    print("🔍 Checking directory structure...")
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # Check if we're in the right place
    if not current_dir.endswith('new-grpc-api'):
        print("❌ You should run this from the new-grpc-api directory")
        print(f"Current dir ends with: {os.path.basename(current_dir)}")
        return False
    
    # Go up one level to new_version
    parent_dir = os.path.dirname(current_dir)
    print(f"Parent directory: {parent_dir}")
    
    # List contents of parent directory
    print(f"\n📁 Contents of {parent_dir}:")
    try:
        for item in os.listdir(parent_dir):
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
    except Exception as e:
        print(f"❌ Could not list directory: {e}")
        return False
    
    # Check for database_schema_sqlalchemy specifically
    db_schema_path = os.path.join(parent_dir, 'database_schema_sqlalchemy')
    print(f"\n🔍 Checking for database schema at: {db_schema_path}")
    
    if os.path.exists(db_schema_path):
        print("✅ database_schema_sqlalchemy directory found!")
        
        # Check its contents
        print(f"\n📁 Contents of database_schema_sqlalchemy:")
        for item in os.listdir(db_schema_path):
            item_path = os.path.join(db_schema_path, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
        
        # Check for database_layer specifically
        database_layer_path = os.path.join(db_schema_path, 'database_layer')
        if os.path.exists(database_layer_path):
            print("✅ database_layer subdirectory found!")
            
            # Check if models exist
            models_path = os.path.join(database_layer_path, 'models')
            if os.path.exists(models_path):
                print("✅ models subdirectory found!")
                
                # List some key model files
                key_files = ['__init__.py', 'app_user.py', 'user_type.py']
                for key_file in key_files:
                    file_path = os.path.join(models_path, key_file)
                    if os.path.exists(file_path):
                        print(f"  ✅ {key_file}")
                    else:
                        print(f"  ❌ {key_file} (missing)")
                
                return True
            else:
                print("❌ models subdirectory not found!")
        else:
            print("❌ database_layer subdirectory not found!")
    else:
        print("❌ database_schema_sqlalchemy directory not found!")
        
        # Suggest where it might be
        print(f"\n💡 Looking for alternative locations...")
        alternative_paths = [
            os.path.join(parent_dir, 'database-schema-sqlalchemy'),
            os.path.join(parent_dir, 'database_schema'),
            os.path.join(current_dir, 'database_schema_sqlalchemy'),
        ]
        
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                print(f"  Found alternative: {alt_path}")
            else:
                print(f"  Not found: {alt_path}")
    
    return False

def suggest_fix():
    print(f"\n🔧 Suggested fixes:")
    print(f"1. Make sure you have the database_schema_sqlalchemy directory")
    print(f"2. It should be in the same parent directory as new-grpc-api")
    print(f"3. Directory structure should be:")
    print(f"   new_version/")
    print(f"   ├── database_schema_sqlalchemy/")
    print(f"   │   └── database_layer/")
    print(f"   │       └── models/")
    print(f"   │           ├── __init__.py")
    print(f"   │           ├── app_user.py")
    print(f"   │           └── user_type.py")
    print(f"   └── new-grpc-api/")
    print(f"       └── src/")
    print(f"")
    print(f"4. If you don't have it, copy it from the original location")
    print(f"5. Or, run the services in mock mode by updating local_config.py:")
    print(f"   \"datasource\": \"mock\"")

if __name__ == "__main__":
    print("=" * 60)
    print("Directory Structure Checker")
    print("=" * 60)
    
    success = check_structure()
    
    if not success:
        suggest_fix()
    else:
        print(f"\n✅ Directory structure looks good!")
        print(f"The services should be able to find the SQLAlchemy models.")