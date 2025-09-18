from dataclasses import dataclass
from codegen.error.user_error_pb2 import UserError
from domain.user import User, CreateUserData

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserCommand:
    user_data: CreateUserData

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserCommandResult:
    user: User = None
    errors: list[UserError] = None
