from dataclasses import dataclass
from codegen.error.user_error_pb2 import UserError
from domain.business import Business

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateBusinessCommand:
    business_name: str
    email: str
    website_url: str = None
    phone_number: str = None
    location_city: str = None
    location_state: str = None
    ein: str = None
    business_description: str = ""
    business_size: str = "SMALL"
    user_email: str = None  # Email of the user creating the business

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateBusinessCommandResult:
    business: Business = None
    errors: list[UserError] = None
