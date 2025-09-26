# src/features/business/create_business/server.py
import concurrent.futures
import grpc
from grpc_reflection.v1alpha import reflection

from codegen.business import create_business_service_pb2, create_business_service_pb2_grpc

from .create_business_service import CreateBusinessService

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    create_business_service_pb2_grpc.add_CreateBusinessServiceServicer_to_server(
        CreateBusinessService(), server
    )
    SERVICE_NAMES = (
        create_business_service_pb2.DESCRIPTOR.services_by_name['CreateBusinessService'].full_name,
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:63000')

    try: 
        print("CreateBusiness gRPC server starting on port 63000...")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Exiting process via KeyboardInterrupt')

if __name__ == '__main__':
    serve()
