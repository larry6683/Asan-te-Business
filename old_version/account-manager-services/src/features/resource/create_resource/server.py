import concurrent.futures
import grpc
from grpc_reflection.v1alpha import reflection

from codegen.resource import create_resource_service_pb2, create_resource_service_pb2_grpc

from .create_resource_service import CreateResourceService

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    create_resource_service_pb2_grpc.add_CreateResourceServiceServicer_to_server(CreateResourceService(), server)
    SERVICE_NAMES = (
        create_resource_service_pb2.DESCRIPTOR.services_by_name['CreateResourceService'].full_name,
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:60000')

    try: 
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Exiting process via KeyboardInterrupt')

if __name__ == '__main__':
    serve()