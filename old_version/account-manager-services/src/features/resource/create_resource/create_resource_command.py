from dataclasses import dataclass
from codegen.error.account_error_pb2 import AccountError
from domain.entity import Entity
from database.models.resource import ResourceCategoryCode

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateResourceCommand:
    entity: Entity
    name: str
    description: str
    category: ResourceCategoryCode

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateResourceCommandResult:
    resource_id: str = None
    errors: list[AccountError] = None