from api.mapper.response_mapper import ResponseMapper
from api.mapper.command_mapper import CommandMapper
from converters.user_converter import UserConverter

from codegen.user.create_user_pb2 import CreateUserRequest, CreateUserResponse

from .create_user_command import CreateUserCommand, CreateUserCommandResult

class CreateUserMapper(
    CommandMapper[CreateUserRequest, CreateUserCommand],
    ResponseMapper[CreateUserCommandResult, CreateUserResponse]
):
    @classmethod
    def to_command(cls, request: CreateUserRequest) -> CreateUserCommand:
        return CreateUserCommand(
            email=request.user.email,
            user_type=request.user.user_type,
            mailing_list_signup=request.user.mailing_list_signup
        )

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
