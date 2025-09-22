import grpc
import sys
sys.path.append('src')

from codegen.user import create_user_pb2, create_user_service_pb2_grpc

def test_create_user():
    # Create channel
    with grpc.insecure_channel('localhost:62000') as channel:
        stub = create_user_service_pb2_grpc.CreateUserServiceStub(channel)
        
        # Test valid user creation
        print("Testing valid user creation...")
        request = create_user_pb2.CreateUserRequest(
            user=create_user_pb2.CreateUserRequest.User(
                email="testuser@example.com",
                user_type="BUSINESS",
                mailing_list_signup=True
            )
        )
        response = stub.CreateUser(request)
        print(f"Response: {response}")
        
        # Test duplicate email
        print("\nTesting duplicate email...")
        request = create_user_pb2.CreateUserRequest(
            user=create_user_pb2.CreateUserRequest.User(
                email="admin@business1.com",
                user_type="BUSINESS",
                mailing_list_signup=False
            )
        )
        response = stub.CreateUser(request)
        print(f"Response: {response}")
        
        # Test invalid user type
        print("\nTesting invalid user type...")
        request = create_user_pb2.CreateUserRequest(
            user=create_user_pb2.CreateUserRequest.User(
                email="invalid@example.com",
                user_type="INVALID_TYPE",
                mailing_list_signup=False
            )
        )
        response = stub.CreateUser(request)
        print(f"Response: {response}")

if __name__ == '__main__':
    test_create_user()
