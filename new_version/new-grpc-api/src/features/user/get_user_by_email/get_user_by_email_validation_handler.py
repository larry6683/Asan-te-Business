import re
from typing import List
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils

from codegen.error.user_error_pb2 import UserError
from codegen.user.get_user_by_email_pb2 import GetUserByEmailRequest

class GetUserByEmailValidationHandler(
    RequestHandler[GetUserByEmailRequest, List[UserError]],
):
    def __init__(self):
        pass

    def handle(self, request: GetUserByEmailRequest) -> List[UserError]:
        errors = []
        
        print(f"Validating request: {request}")  # Debug log
        
        # Check if email is provided
        if not request.email or request.email.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("email"))
            return errors
        
        # Check email format
        if not self._is_valid_email(request.email):
            errors.append(ErrorUtils.create_parameter_error("Invalid email format"))
            
        print(f"Validation errors: {errors}")  # Debug log
        return errors
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
