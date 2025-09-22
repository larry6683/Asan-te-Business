from config.config import Config
from database.db_utils import DBUtils
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils
from utils.enum_utils import EnumUtils

from domain.entity import Entity

from database.models.business_user import BusinessUserPermissionRoleCode

from codegen.auth.auth_pb2 import Auth
from codegen.error.account_error_code_pb2 import AccountErrorCode as ErrorCode
from codegen.error.account_error_pb2 import AccountError as Error
from codegen.auth.entity_type_pb2 import EntityType

from .auth_request import AuthRequest
from converters.entity_converter import EntityConverter

from database.db_data.business_users import query_business_user_permission

# eventually a lot of this will be offloaded to kubernetes
class AuthHandler(
    RequestHandler[AuthRequest, list[Error]],
):
    def __init__(self):
        # define services
        pass

    def handle(self, request: AuthRequest) -> list[Error]:
        errors = []
        if auth_param_errors := self.ValidateParameters(request.auth):
            return auth_param_errors
        
        # destructured for reusability
        if auth_errors := self.Authenticate(
            EntityConverter.to_domain(request.auth), 
            request.auth.user.id,
            request.required_permission_role,
            request.operation
        ):
            errors.extend(auth_errors)
        
        return errors
    
    def ValidateParameters(self, auth: Auth):
        errors = []

        if not auth.user.id:
            errors.append(ErrorUtils.create_required_parameter_error('auth.user.id'))
        if not auth.entity.entity_type:
            errors.append(ErrorUtils.create_required_parameter_error('auth.entity.entity_type'))
        if not auth.entity.id:
            errors.append(ErrorUtils.create_required_parameter_error('auth.entity.id'))

        if auth.entity.entity_type not in [EntityType.ENTITY_BUSINESS]:
            errors.append(ErrorUtils.create_parameter_error(f'parameter: entity_type: {EnumUtils.get_enum_name(EntityType, auth.entity.entity_type)} is not supported.'))
        
        return errors
    
    # destructured for reusability
    def Authenticate(self, 
            entity: Entity,
            app_user_id: str,
            required_permission_role: BusinessUserPermissionRoleCode, 
            operation = ""
    ) -> list[Error]:
        errors: list[Error] = []
        
        business_user_permission_role = None
        
        if Config.use_db():
            business_user_permission_role = self.query_db(entity, app_user_id) 
        else:
            business_user_permission_role = query_business_user_permission(entity.id, app_user_id)

        if not business_user_permission_role:
            errors.append(ErrorUtils.create_error(
                ErrorCode.ERROR_ENTITY_USER_NOT_FOUND, 
                f'cannot find user with id: {app_user_id} belonging to entity with id {entity.id}')
            )
            return errors
        
        if (business_user_permission_role != BusinessUserPermissionRoleCode.ADMIN
                and business_user_permission_role != required_permission_role):
            errors.append(ErrorUtils.create_error(
                ErrorCode.ERROR_INVALID_PERMISSION_ROLE, 
                f'user with id: {app_user_id} does not have permission to permission to execute operation: {operation.__name__ if callable(operation) else operation}')
            )
            return errors
        
        return errors
    
    def query_db(self, entity: Entity, app_user_id: str) -> BusinessUserPermissionRoleCode:
        sql = """ --sql
            SELECT  bupr.code
            FROM    app_user au
            JOIN    business_user bu 
                ON  au.app_user_id = bu.app_user_id
            JOIN    business_user_permission_role bupr 
                ON  bupr.business_user_permission_role_id = bu.business_user_permission_role_id
            WHERE bu.business_id = %(business_id)s
            AND au.app_user_id = %(app_user_id)s;
            """
        params = {
            "business_id": entity.id,
            "app_user_id": app_user_id
        }
        
        try:
            with DBUtils.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    result = cursor.fetchone()
                    return BusinessUserPermissionRoleCode(int(result[0])) if result else None
        except Exception as e:
            print(f"Error querying database: {e}")
            raise e