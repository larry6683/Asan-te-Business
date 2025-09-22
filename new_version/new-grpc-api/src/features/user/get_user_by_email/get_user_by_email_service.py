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
            if errors := self.validation_handler.handle(request):
                return GetUserByEmailResponse(errors=errors)
            
            query = Mapper.to_query(request)
            result = self.query_handler.handle(query)
            
            return Mapper.to_response(result)
        
        except Exception as e:
            return GetUserByEmailResponse(
                errors=[ErrorUtils.create_operation_failed_error(self.GetUserByEmail, str(e), e)]
            )
