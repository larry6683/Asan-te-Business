# src/database_path_fix.py
import sys
import os

def import_sqlalchemy_models(model_names=None):
    """Helper to import SQLAlchemy models with proper path handling"""
    if model_names is None:
        model_names = ['AppUser', 'UserType']
    
    try:
        # Get the current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Navigate up to find the database_schema_sqlalchemy directory
        # From: new_version/new-grpc-api/src/database_path_fix.py
        # To:   new_version/database_schema_sqlalchemy/
        
        # Go up from src to new-grpc-api, then to new_version, then to database_schema_sqlalchemy
        grpc_api_dir = os.path.dirname(current_dir)  # new-grpc-api
        new_version_dir = os.path.dirname(grpc_api_dir)  # new_version
        db_schema_path = os.path.join(new_version_dir, 'database_schema_sqlalchemy')
        
        print(f"Looking for database schema at: {db_schema_path}")
        
        if os.path.exists(db_schema_path):
            if db_schema_path not in sys.path:
                sys.path.insert(0, db_schema_path)
            print(f"Added to sys.path: {db_schema_path}")
        else:
            print(f"Database schema path not found: {db_schema_path}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Current file location: {current_dir}")
            # Try alternative paths
            alt_paths = [
                os.path.join(os.getcwd(), 'database_schema_sqlalchemy'),
                os.path.join(os.path.dirname(os.getcwd()), 'database_schema_sqlalchemy'),
                os.path.join(current_dir, '..', '..', '..', 'database_schema_sqlalchemy'),
            ]
            for alt_path in alt_paths:
                abs_alt_path = os.path.abspath(alt_path)
                print(f"Trying alternative path: {abs_alt_path}")
                if os.path.exists(abs_alt_path):
                    if abs_alt_path not in sys.path:
                        sys.path.insert(0, abs_alt_path)
                    db_schema_path = abs_alt_path
                    print(f"Found and added alternative path: {abs_alt_path}")
                    break
            else:
                raise ImportError(f"Could not find database_schema_sqlalchemy directory")
        
        # Import the models
        print("Attempting to import SQLAlchemy models...")
        from database_layer.models.app_user import AppUser
        from database_layer.models.user_type import UserType
        from database_layer.models.business import Business
        from database_layer.models.business_size import BusinessSize
        from database_layer.models.business_user import BusinessUser
        from database_layer.models.business_user_permission_role import BusinessUserPermissionRole
        
        print("✓ SQLAlchemy models imported successfully")
        
        # Create a mapping of model names to actual models
        model_map = {
            'AppUser': AppUser,
            'UserType': UserType,
            'Business': Business,
            'BusinessSize': BusinessSize,
            'BusinessUser': BusinessUser,
            'BusinessUserPermissionRole': BusinessUserPermissionRole
        }
        
        # Return requested models
        result_models = []
        for name in model_names:
            if name in model_map:
                result_models.append(model_map[name])
            else:
                print(f"Warning: Model '{name}' not found in model_map")
                result_models.append(None)
        
        # Add SQLALCHEMY_AVAILABLE flag
        result_models.append(True)
        
        return tuple(result_models)
        
    except ImportError as e:
        print(f"SQLAlchemy models import failed: {e}")
        print(f"sys.path: {sys.path}")
        # Return None for each requested model plus False for availability
        return tuple([None] * len(model_names) + [False])
    except Exception as e:
        print(f"Unexpected error importing SQLAlchemy models: {e}")
        return tuple([None] * len(model_names) + [False])
