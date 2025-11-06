import grpc
from concurrent import futures
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpc_reflection.v1alpha import reflection
from codegen.analytics import analytics_pb2, analytics_pb2_grpc
from services.analytics.analytics_service import AnalyticsService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(AnalyticsService(), server)
    
    SERVICE_NAMES = (
        analytics_pb2.DESCRIPTOR.services_by_name['AnalyticsService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50054')
    print('Analytics Service started on port 50054')
    print('Service endpoints:')
    print('  - TrackStep: Track registration step interactions')
    print('  - CompleteStep: Mark steps as completed')
    print('  - GetRegistrationSteps: Get all registration steps')
    print('  - GetUserJourney: Get user registration journey')
    print('  - GetSessionJourney: Get session registration journey')
    print('  - GetRegistrationStats: Get registration statistics')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()