import re
from typing import List
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils

from codegen.error.user_error_pb2 import UserError
from codegen.business.create_business_pb2 import CreateBusinessRequest

class CreateBusinessValidationHandler(
    RequestHandler[CreateBusinessRequest, List[UserError]],
):
    VALID_BUSINESS_SIZES = ['SMALL', 'MEDIUM', 'LARGE']

    def __init__(self):
        pass

    def handle(self, request: CreateBusinessRequest) -> List[UserError]:
        errors = []
        
        print(f"Validating create business request: {request}")  # Debug log
        
        # Check if business object exists
        if not request.business:
            errors.append(ErrorUtils.create_required_parameter_error("business"))
            return errors

        # Validate business_name
        if not request.business.business_name or request.business.business_name.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("business.business_name"))
        
        # Validate email
        if not request.business.email or request.business.email.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("business.email"))
        elif not self._is_valid_email(request.business.email):
            errors.append(ErrorUtils.create_parameter_error("Invalid email format"))
        
        # Validate location_city (required)
        if not request.business.location_city or request.business.location_city.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("business.location_city"))
        
        # Validate location_state (required)
        if not request.business.location_state or request.business.location_state.strip() == "":
            errors.append(ErrorUtils.create_required_parameter_error("business.location_state"))
        
        # Validate business_size
        if request.business.business_size and request.business.business_size.upper() not in self.VALID_BUSINESS_SIZES:
            errors.append(ErrorUtils.create_parameter_error(
                f"Invalid business_size. Must be one of: {', '.join(self.VALID_BUSINESS_SIZES)}"
            ))
        
        # Validate user_email if provided
        if request.user_email and not self._is_valid_email(request.user_email):
            errors.append(ErrorUtils.create_parameter_error("Invalid user_email format"))
        
        # Validate website_url if provided
        if request.business.website_url and not self._is_valid_url(request.business.website_url):
            errors.append(ErrorUtils.create_parameter_error("Invalid website_url format"))
        
        print(f"Create business validation errors: {errors}")  # Debug log
        return errors
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation"""
        if not isinstance(url, str):
            return False
        pattern = r'^https?://.+\..+'
        return bool(re.match(pattern, url))
