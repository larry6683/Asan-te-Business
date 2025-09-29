import grpc
from concurrent import futures
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpc_reflection.v1alpha import reflection
from codegen.user import user_pb2, user_pb2_grpc
from services.user.user_service import UserService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    
    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name['UserService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    print('User Service started on port 50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
