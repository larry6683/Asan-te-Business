import concurrent.futures
import grpc
from grpc_reflection.v1alpha import reflection

from codegen.user import get_user_by_email_service_pb2, get_user_by_email_service_pb2_grpc

from .get_user_by_email_service import GetUserByEmailService

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    get_user_by_email_service_pb2_grpc.add_GetUserByEmailServiceServicer_to_server(
        GetUserByEmailService(), server
    )
    SERVICE_NAMES = (
        get_user_by_email_service_pb2.DESCRIPTOR.services_by_name['GetUserByEmailService'].full_name,
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:61000')

    try: 
        print("GetUserByEmail gRPC server starting on port 61000...")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Exiting process via KeyboardInterrupt')

if __name__ == '__main__':
    serve()
