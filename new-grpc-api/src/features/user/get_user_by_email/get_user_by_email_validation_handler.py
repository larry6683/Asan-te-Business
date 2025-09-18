import re
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils

from codegen.error.user_error_pb2 import UserError
from codegen.user.get_user_by_email_pb2 import GetUserByEmailRequest

class GetUserByEmailValidationHandler(
    RequestHandler[GetUserByEmailRequest, list[UserError]],
):
    def __init__(self):
        pass

    def handle(self, request: GetUserByEmailRequest) -> list[UserError]:
        errors = []

        if not request.email:
            errors.append(ErrorUtils.create_required_parameter_error("email"))
        elif not self._is_valid_email(request.email):
            errors.append(ErrorUtils.create_parameter_error("Invalid email format"))
            
        return errors
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
