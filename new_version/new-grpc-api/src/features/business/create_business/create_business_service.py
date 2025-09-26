from error.error_utils import ErrorUtils

from codegen.business.create_business_pb2 import CreateBusinessRequest, CreateBusinessResponse
from codegen.business.create_business_service_pb2_grpc import CreateBusinessServiceServicer

from .create_business_validation_handler import CreateBusinessValidationHandler
from .create_business_command_handler import CreateBusinessCommandHandler
from .create_business_mapper import CreateBusinessMapper as Mapper

class CreateBusinessService(CreateBusinessServiceServicer):
    def __init__(self):
        self.validation_handler = CreateBusinessValidationHandler()
        self.command_handler = CreateBusinessCommandHandler()

    def CreateBusiness(self, request: CreateBusinessRequest, context):
        try:
            print(f"Received create business request: {request}")  # Debug log
            
            # Validate request
            validation_errors = self.validation_handler.handle(request)
            if validation_errors:
                print(f"Create business validation failed: {validation_errors}")  # Debug log
                response = CreateBusinessResponse()
                response.errors.extend(validation_errors)
                return response
            
            # Process command
            command = Mapper.to_command(request)
            result = self.command_handler.handle(command)
            
            # Map response
            response = Mapper.to_response(result)
            print(f"Sending create business response: {response}")  # Debug log
            return response
        
        except Exception as e:
            print(f"Create business service error: {e}")  # Debug log
            import traceback
            traceback.print_exc()
            
            response = CreateBusinessResponse()
            error = ErrorUtils.create_operation_failed_error(self.CreateBusiness, str(e), e)
            response.errors.append(error)
            return response
