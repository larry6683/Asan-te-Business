import sys
sys.path.append('src')

import grpc
import concurrent.futures
from grpc_reflection.v1alpha import reflection

# Test if the generated files work
try:
    from codegen.user import get_user_by_email_pb2, get_user_by_email_service_pb2_grpc
    from codegen.user import create_user_pb2, create_user_service_pb2_grpc
    from codegen.error import user_error_pb2
    print("✅ All protobuf imports successful!")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Simple test service
class TestGetUserService(get_user_by_email_service_pb2_grpc.GetUserByEmailServiceServicer):
    def GetUserByEmail(self, request, context):
        print(f"Received request: {request}")
        response = get_user_by_email_pb2.GetUserByEmailResponse()
        
        if request.email == "test@example.com":
            response.user.id = "test-id"
            response.user.email = request.email
            response.user.user_type = "BUSINESS"
        else:
            error = response.errors.add()
            error.error_code = user_error_pb2.UserErrorCode.ERROR_USER_EMAIL_NOT_FOUND
            error.detail = f"User with email '{request.email}' not found"
        
        return response

class TestCreateUserService(create_user_service_pb2_grpc.CreateUserServiceServicer):
    def CreateUser(self, request, context):
        print(f"Received request: {request}")
        response = create_user_pb2.CreateUserResponse()
        
        if request.user.email and "@" in request.user.email:
            response.user.id = "new-test-id"
            response.user.email = request.user.email
            response.user.user_type = request.user.user_type
        else:
            error = response.errors.add()
            error.error_code = user_error_pb2.UserErrorCode.ERROR_INVALID_PARAMETER
            error.detail = "Invalid email format"
        
        return response

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    
    # Add services
    get_user_by_email_service_pb2_grpc.add_GetUserByEmailServiceServicer_to_server(
        TestGetUserService(), server
    )
    create_user_service_pb2_grpc.add_CreateUserServiceServicer_to_server(
        TestCreateUserService(), server
    )
    
    # Enable reflection
    SERVICE_NAMES = (
        get_user_by_email_service_pb2.DESCRIPTOR.services_by_name['GetUserByEmailService'].full_name,
        create_user_service_pb2.DESCRIPTOR.services_by_name['CreateUserService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    # Start servers
    server.add_insecure_port('[::]:61000')
    server.add_insecure_port('[::]:62000')
    
    print("✅ Test gRPC servers starting...")
    print("GetUserByEmail: localhost:61000")
    print("CreateUser: localhost:62000")
    
    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == '__main__':
    serve()
