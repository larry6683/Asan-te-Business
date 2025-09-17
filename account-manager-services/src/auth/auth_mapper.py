from database.models.business_user import BusinessUserPermissionRoleCode
from domain.entity import Entity
from .auth_request import AuthRequest
from codegen.auth.auth_pb2 import Auth
from converters.entity_type_converter import EntityTypeConverter

class AuthMapper:
    
    @staticmethod
    def to_auth_request(
        auth: Auth, 
        required_permission_role: BusinessUserPermissionRoleCode,
        operation: str = None
    ) -> AuthRequest:
        return AuthRequest(
            auth=auth,
            required_permission_role=required_permission_role,
            operation=operation
        )