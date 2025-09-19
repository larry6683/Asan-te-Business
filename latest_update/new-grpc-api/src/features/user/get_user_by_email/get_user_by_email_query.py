from dataclasses import dataclass
from codegen.error.user_error_pb2 import UserError
from domain.user import User

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserByEmailQuery:
    email: str

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserByEmailQueryResult:
    user: User = None
    errors: list[UserError] = None
