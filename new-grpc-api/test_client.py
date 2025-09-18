import grpc
import sys
sys.path.append('src')

from codegen.user import get_user_by_email_pb2, get_user_by_email_service_pb2_grpc

def test_get_user_by_email():
    # Create channel
    with grpc.insecure_channel('localhost:61000') as channel:
        stub = get_user_by_email_service_pb2_grpc.GetUserByEmailServiceStub(channel)
        
        # Test valid email
        print("Testing valid email...")
        request = get_user_by_email_pb2.GetUserByEmailRequest(
            email="admin@business1.com"
        )
        response = stub.GetUserByEmail(request)
        print(f"Response: {response}")
        
        # Test invalid email
        print("\nTesting invalid email...")
        request = get_user_by_email_pb2.GetUserByEmailRequest(
            email="nonexistent@email.com"
        )
        response = stub.GetUserByEmail(request)
        print(f"Response: {response}")
        
        # Test empty email
        print("\nTesting empty email...")
        request = get_user_by_email_pb2.GetUserByEmailRequest(
            email=""
        )
        response = stub.GetUserByEmail(request)
        print(f"Response: {response}")

if __name__ == '__main__':
    test_get_user_by_email()
