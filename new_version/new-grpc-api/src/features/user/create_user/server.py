import concurrent.futures
import grpc
from grpc_reflection.v1alpha import reflection

from codegen.user import create_user_service_pb2, create_user_service_pb2_grpc

from .create_user_service import CreateUserService

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    create_user_service_pb2_grpc.add_CreateUserServiceServicer_to_server(
        CreateUserService(), server
    )
    SERVICE_NAMES = (
        create_user_service_pb2.DESCRIPTOR.services_by_name['CreateUserService'].full_name,
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:62000')

    try: 
        print("CreateUser gRPC server starting on port 62000...")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Exiting process via KeyboardInterrupt')

if __name__ == '__main__':
    serve()
