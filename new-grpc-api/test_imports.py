import sys
sys.path.append('src')

try:
    print("Testing imports...")
    
    # Test basic imports
    from features.user.create_user.create_user_service import CreateUserService
    print("✓ CreateUserService imported successfully")
    
    from codegen.user import create_user_pb2, create_user_service_pb2_grpc
    print("✓ Protobuf files imported successfully")
    
    from features.user.create_user.create_user_command_handler import CreateUserCommandHandler
    print("✓ Command handler imported successfully")
    
    print("All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
