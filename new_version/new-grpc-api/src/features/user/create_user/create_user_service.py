from error.error_utils import ErrorUtils

from codegen.user.create_user_pb2 import CreateUserRequest, CreateUserResponse
from codegen.user.create_user_service_pb2_grpc import CreateUserServiceServicer

from .create_user_validation_handler import CreateUserValidationHandler
from .create_user_command_handler import CreateUserCommandHandler
from .create_user_mapper import CreateUserMapper as Mapper

class CreateUserService(CreateUserServiceServicer):
    def __init__(self):
        self.validation_handler = CreateUserValidationHandler()
        self.command_handler = CreateUserCommandHandler()

    def CreateUser(self, request: CreateUserRequest, context):
        try:
            print(f"Received create user request: {request}")  # Debug log
            
            # Validate request
            validation_errors = self.validation_handler.handle(request)
            if validation_errors:
                print(f"Create user validation failed: {validation_errors}")  # Debug log
                response = CreateUserResponse()
                response.errors.extend(validation_errors)
                return response
            
            # Process command
            command = Mapper.to_command(request)
            result = self.command_handler.handle(command)
            
            # Map response
            response = Mapper.to_response(result)
            print(f"Sending create user response: {response}")  # Debug log
            return response
        
        except Exception as e:
            print(f"Create user service error: {e}")  # Debug log
            import traceback
            traceback.print_exc()
            
            response = CreateUserResponse()
            error = ErrorUtils.create_operation_failed_error(self.CreateUser, str(e), e)
            response.errors.append(error)
            return response
