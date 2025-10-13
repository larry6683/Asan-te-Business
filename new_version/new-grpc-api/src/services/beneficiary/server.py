import grpc
from concurrent import futures
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpc_reflection.v1alpha import reflection
from codegen.beneficiary import beneficiary_pb2, beneficiary_pb2_grpc
from services.beneficiary.beneficiary_service import BeneficiaryService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    beneficiary_pb2_grpc.add_BeneficiaryServiceServicer_to_server(BeneficiaryService(), server)
    
    SERVICE_NAMES = (
        beneficiary_pb2.DESCRIPTOR.services_by_name['BeneficiaryService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50053')
    print('Beneficiary Service started on port 50053')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
