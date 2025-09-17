import concurrent.futures
import grpc
from grpc_reflection.v1alpha import reflection

# replace this comment with service import statements

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    # replace these comments with function call to:
    # x_service_pb2_grpc.x_serviceServiceServicer_to_server
    SERVICE_NAMES = (
        # replace these comments with item:
        # x_service_pb2.DESCRIPTOR.services_by_name['x_service'].full_name
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:######')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()