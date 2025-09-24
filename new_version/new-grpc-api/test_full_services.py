import sys
sys.path.append('src')

import grpc
import concurrent.futures
from grpc_reflection.v1alpha import reflection

try:
    from codegen.user import get_user_by_email_service_pb2, get_user_by_email_service_pb2_grpc
    from codegen.user import create_user_service_pb2, create_user_service_pb2_grpc
    
    from features.user.get_user_by_email.get_user_by_email_service import GetUserByEmailService
    from features.user.create_user.create_user_service import CreateUserService
    
    print("✅ All imports successful!")
except Exception as e:
    import traceback
    print(f"❌ Import error: {e}")
    print(traceback.format_exc())
    exit(1)

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    
    # Add GetUserByEmail service
    get_user_by_email_service_pb2_grpc.add_GetUserByEmailServiceServicer_to_server(
        GetUserByEmailService(), server
    )
    
    # Add CreateUser service  
    create_user_service_pb2_grpc.add_CreateUserServiceServicer_to_server(
        CreateUserService(), server
    )
    
    # Enable reflection
    SERVICE_NAMES = (
        get_user_by_email_service_pb2.DESCRIPTOR.services_by_name['GetUserByEmailService'].full_name,
        create_user_service_pb2.DESCRIPTOR.services_by_name['CreateUserService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    # Bind to different ports
    server.add_insecure_port('[::]:61000')  # GetUserByEmail
    server.add_insecure_port('[::]:62000')  # CreateUser
    
    print("✅ Full gRPC services starting...")
    print("GetUserByEmail: localhost:61000")
    print("CreateUser: localhost:62000")
    print("Both services are running on the same server instance")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == '__main__':
    serve()
