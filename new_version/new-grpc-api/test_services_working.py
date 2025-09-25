# new_version/new-grpc-api/test_services_working.py
"""Test that the gRPC services are working with mock data"""

import sys
sys.path.append('src')

import grpc
import time

def test_get_user_by_email():
    """Test GetUserByEmail service"""
    print("🧪 Testing GetUserByEmail service...")
    
    try:
        from codegen.user import get_user_by_email_pb2, get_user_by_email_service_pb2_grpc
        
        with grpc.insecure_channel('localhost:61000') as channel:
            stub = get_user_by_email_service_pb2_grpc.GetUserByEmailServiceStub(channel)
            
            # Test existing user
            print("Testing existing user...")
            request = get_user_by_email_pb2.GetUserByEmailRequest(
                email='admin@business1.com'
            )
            response = stub.GetUserByEmail(request)
            
            if response.user and response.user.email:
                print(f"✅ Found user: {response.user.email} ({response.user.user_type})")
            else:
                print(f"❌ User not found or error: {response.errors}")
            
            # Test non-existing user
            print("Testing non-existing user...")
            request = get_user_by_email_pb2.GetUserByEmailRequest(
                email='nonexistent@example.com'
            )
            response = stub.GetUserByEmail(request)
            
            if response.errors:
                print(f"✅ Correctly returned error for non-existent user")
            else:
                print(f"❌ Should have returned error for non-existent user")
                
    except Exception as e:
        print(f"❌ GetUserByEmail test failed: {e}")
        import traceback
        traceback.print_exc()

def test_create_user():
    """Test CreateUser service"""
    print("\n🧪 Testing CreateUser service...")
    
    try:
        from codegen.user import create_user_pb2, create_user_service_pb2_grpc
        
        with grpc.insecure_channel('localhost:62000') as channel:
            stub = create_user_service_pb2_grpc.CreateUserServiceStub(channel)
            
            # Test creating new user
            print("Testing user creation...")
            request = create_user_pb2.CreateUserRequest(
                user=create_user_pb2.CreateUserRequest.User(
                    email="newuser@example.com",
                    user_type="BUSINESS",
                    mailing_list_signup=True
                )
            )
            response = stub.CreateUser(request)
            
            if response.user and response.user.email:
                print(f"✅ Created user: {response.user.email} ({response.user.user_type})")
                print(f"   User ID: {response.user.id}")
            else:
                print(f"❌ Failed to create user: {response.errors}")
            
            # Test duplicate email (should fail)
            print("Testing duplicate email...")
            request = create_user_pb2.CreateUserRequest(
                user=create_user_pb2.CreateUserRequest.User(
                    email="admin@business1.com",  # This should already exist
                    user_type="CONSUMER", 
                    mailing_list_signup=False
                )
            )
            response = stub.CreateUser(request)
            
            if response.errors:
                print(f"✅ Correctly rejected duplicate email")
            else:
                print(f"❌ Should have rejected duplicate email")
                
    except Exception as e:
        print(f"❌ CreateUser test failed: {e}")
        import traceback
        traceback.print_exc()

def check_services_running():
    """Check if services are running"""
    print("🔍 Checking if services are running...")
    
    services = [
        ("GetUserByEmail", "localhost:61000"),
        ("CreateUser", "localhost:62000")
    ]
    
    for service_name, address in services:
        try:
            with grpc.insecure_channel(address) as channel:
                # Try to connect with a short timeout
                grpc.channel_ready_future(channel).result(timeout=2)
                print(f"✅ {service_name} is running on {address}")
        except:
            print(f"❌ {service_name} is NOT running on {address}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Testing gRPC Services")
    print("=" * 50)
    
    if not check_services_running():
        print("\n💡 Start the services first:")
        print("   ./tools/run/run_all.sh")
        print("   or")
        print("   ./start_services_debug.sh")
        sys.exit(1)
    
    print()
    test_get_user_by_email()
    test_create_user()
    
    print("\n" + "=" * 50)
    print("🎉 Service tests completed!")