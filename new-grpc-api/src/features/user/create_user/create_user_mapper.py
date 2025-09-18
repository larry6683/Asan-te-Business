from api.mapper.response_mapper import ResponseMapper
from api.mapper.command_mapper import CommandMapper
from converters.user_converter import UserConverter
from domain.user import CreateUserData

from codegen.user.create_user_pb2 import CreateUserRequest, CreateUserResponse

from .create_user_command import CreateUserCommand, CreateUserCommandResult

class CreateUserMapper(
    CommandMapper[CreateUserRequest, CreateUserCommand],
    ResponseMapper[CreateUserCommandResult, CreateUserResponse]
):
    @classmethod
    def to_command(cls, request: CreateUserRequest) -> CreateUserCommand:
        user_type = UserConverter.user_type_from_string(request.user_data.user_type)
        
        user_data = CreateUserData(
            email=request.user_data.email,
            user_type=user_type,
            mailing_list_signup=request.user_data.mailing_list_signup
        )
        
        return CreateUserCommand(user_data=user_data)

    @classmethod
    def to_response(cls, result: CreateUserCommandResult) -> CreateUserResponse:
        if result.errors:
            return CreateUserResponse(
                errors=result.errors
            )

        return CreateUserResponse(
            user=CreateUserResponse.User(
                id=result.user.id,
                email=result.user.email,
                user_type=UserConverter.user_type_to_string(result.user.user_type)
            )
        )
