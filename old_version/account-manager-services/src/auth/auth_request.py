from dataclasses import dataclass
from typing import Any
from codegen.auth.auth_pb2 import Auth
from database.models.business_user import BusinessUserPermissionRoleCode
from domain.entity import Entity

@dataclass(slots=True)
class AuthRequest:
    auth: Auth
    required_permission_role: BusinessUserPermissionRoleCode
    operation: Any