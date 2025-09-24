import re
from typing import List
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils

from codegen.error.user_error_pb2 import UserError
from codegen.user.create_user_pb2 import CreateUserRequest

class CreateUserValidationHandler(
    RequestHandler[CreateUserRequest, List[UserError]],
):
    VALID_USER_TYPES = ['BUSINESS', 'BENEFICIARY', 'CONSUMER']

    def __init__(self):
        pass

    def handle(self, request: CreateUserRequest) -> List[UserError]:
        errors = []
        
        print(f"Validating create user request: {request}")  # Debug log
        
        # Check if user object exists
        if not request.user:
            errors.append(ErrorUtils.create_required_parameter_error("user"))
            return errors

        # Validate email
        if not request.user.email or request.user.email.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("user.email"))
        elif not self._is_valid_email(request.user.email):
            errors.append(ErrorUtils.create_parameter_error("Invalid email format"))
        
        # Validate user_type
        if not request.user.user_type or request.user.user_type.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("user.user_type"))
        elif request.user.user_type.upper() not in self.VALID_USER_TYPES:
            errors.append(ErrorUtils.create_parameter_error(
                f"Invalid user_type. Must be one of: {', '.join(self.VALID_USER_TYPES)}"
            ))
        
        print(f"Create user validation errors: {errors}")  # Debug log
        return errors
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
