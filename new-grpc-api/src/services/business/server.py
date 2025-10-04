import grpc
from concurrent import futures
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpc_reflection.v1alpha import reflection
from codegen.business import business_pb2, business_pb2_grpc
from services.business.business_service import BusinessService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    business_pb2_grpc.add_BusinessServiceServicer_to_server(BusinessService(), server)
    
    SERVICE_NAMES = (
        business_pb2.DESCRIPTOR.services_by_name['BusinessService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50052')
    print('Business Service started on port 50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
