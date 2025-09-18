import re
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils

from codegen.error.user_error_pb2 import UserError
from codegen.user.create_user_pb2 import CreateUserRequest

class CreateUserValidationHandler(
    RequestHandler[CreateUserRequest, list[UserError]],
):
    def __init__(self):
        pass

    def handle(self, request: CreateUserRequest) -> list[UserError]:
        errors = []

        # Validate email
        if not request.user_data.email:
            errors.append(ErrorUtils.create_required_parameter_error("user_data.email"))
        elif not self._is_valid_email(request.user_data.email):
            errors.append(ErrorUtils.create_parameter_error("Invalid email format"))
        
        # Validate user_type  
        if not request.user_data.user_type:
            errors.append(ErrorUtils.create_required_parameter_error("user_data.user_type"))
        elif request.user_data.user_type.upper() not in ["BUSINESS", "BENEFICIARY", "CONSUMER"]:
            errors.append(ErrorUtils.create_invalid_user_type_error(request.user_data.user_type))
            
        return errors
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
