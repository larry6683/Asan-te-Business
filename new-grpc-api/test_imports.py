import sys
sys.path.append('src')

try:
    from codegen.user import get_user_by_email_pb2
    print("✓ Successfully imported get_user_by_email_pb2")
except ImportError as e:
    print(f"✗ Failed to import get_user_by_email_pb2: {e}")

try:
    from codegen.user import get_user_by_email_service_pb2_grpc
    print("✓ Successfully imported get_user_by_email_service_pb2_grpc")
except ImportError as e:
    print(f"✗ Failed to import get_user_by_email_service_pb2_grpc: {e}")

try:
    from codegen.error import user_error_pb2
    print("✓ Successfully imported user_error_pb2")
except ImportError as e:
    print(f"✗ Failed to import user_error_pb2: {e}")

try:
    from codegen.auth import auth_pb2
    print("✓ Successfully imported auth_pb2")
except ImportError as e:
    print(f"✗ Failed to import auth_pb2: {e}")
