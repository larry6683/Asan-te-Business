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
            if errors := self.validation_handler.handle(request):
                return CreateUserResponse(errors=errors)
            
            command = Mapper.to_command(request)
            result = self.command_handler.handle(command)
            
            return Mapper.to_response(result)
        
        except Exception as e:
            return CreateUserResponse(
                errors=[ErrorUtils.create_operation_failed_error(self.CreateUser, str(e), e)]
            )
