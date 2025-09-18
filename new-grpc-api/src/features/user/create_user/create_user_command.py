from dataclasses import dataclass
from codegen.error.user_error_pb2 import UserError
from domain.user import User

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserCommand:
    email: str
    user_type: str
    mailing_list_signup: bool

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserCommandResult:
    user: User = None
    errors: list[UserError] = None
