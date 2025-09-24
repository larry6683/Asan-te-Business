from error.error_utils import ErrorUtils

from codegen.user.get_user_by_email_pb2 import GetUserByEmailRequest, GetUserByEmailResponse
from codegen.user.get_user_by_email_service_pb2_grpc import GetUserByEmailServiceServicer

from .get_user_by_email_validation_handler import GetUserByEmailValidationHandler
from .get_user_by_email_query_handler import GetUserByEmailQueryHandler
from .get_user_by_email_mapper import GetUserByEmailMapper as Mapper

class GetUserByEmailService(GetUserByEmailServiceServicer):
    def __init__(self):
        self.validation_handler = GetUserByEmailValidationHandler()
        self.query_handler = GetUserByEmailQueryHandler()

    def GetUserByEmail(self, request: GetUserByEmailRequest, context):
        try:
            print(f"Received request: {request}")  # Debug log
            
            # Validate request
            validation_errors = self.validation_handler.handle(request)
            if validation_errors:
                print(f"Validation failed: {validation_errors}")  # Debug log
                response = GetUserByEmailResponse()
                response.errors.extend(validation_errors)
                return response
            
            # Process query
            query = Mapper.to_query(request)
            result = self.query_handler.handle(query)
            
            # Map response
            response = Mapper.to_response(result)
            print(f"Sending response: {response}")  # Debug log
            return response
        
        except Exception as e:
            print(f"Service error: {e}")  # Debug log
            response = GetUserByEmailResponse()
            error = ErrorUtils.create_operation_failed_error(self.GetUserByEmail, str(e), e)
            response.errors.append(error)
            return response
