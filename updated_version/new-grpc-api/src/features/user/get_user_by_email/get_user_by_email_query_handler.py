from psycopg import Cursor
from config.config import Config
from database.db_utils import DBUtils

from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils
from converters.user_converter import UserConverter

from database.db_data.users import get_user_by_email

from .get_user_by_email_query import GetUserByEmailQuery, GetUserByEmailQueryResult
from codegen.error.user_error_code_pb2 import UserErrorCode

class GetUserByEmailQueryHandler(
    RequestHandler[GetUserByEmailQuery, GetUserByEmailQueryResult]
):
    def __init__(self):
        pass

    def handle(self, request: GetUserByEmailQuery) -> GetUserByEmailQueryResult:
        if not Config.use_db():
            return self.handle_mock(request)
        
        try:
            with DBUtils.get_connection() as conn:
                with conn.cursor() as cursor:
                    return self.handle_with_db(cursor, request)
        except Exception as e:
            return GetUserByEmailQueryResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle, str(e), e)]
            )
    
    def handle_with_db(self, cursor: Cursor, request: GetUserByEmailQuery) -> GetUserByEmailQueryResult:
        """
        Database implementation - to be implemented with SQLAlchemy
        """
        sql = """
            SELECT  au.app_user_id,
                    ut.code,
                    au.email
            FROM    app_user au
            INNER JOIN user_type ut ON au.user_type_id = ut.user_type_id
            WHERE au.email_hash = digest(lower(%(email)s), 'md5')
        """
        params = {"email": request.email}
        
        try:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            
            if not result:
                return GetUserByEmailQueryResult(
                    errors=[ErrorUtils.create_user_not_found_error(request.email)]
                )
            
            # Convert result to domain object
            from database.models.user import UserDbo, UserTypeCode
            user_dbo = UserDbo(
                app_user_id=result[0],
                email=result[2],
                user_type_code=UserTypeCode(result[1])
            )
            
            user = UserConverter.to_domain(user_dbo)
            
            return GetUserByEmailQueryResult(user=user)
            
        except Exception as e:
            return GetUserByEmailQueryResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_with_db, str(e), e)]
            )
        
    def handle_mock(self, request: GetUserByEmailQuery) -> GetUserByEmailQueryResult:
        user_dbo = get_user_by_email(request.email)
        
        if not user_dbo:
            return GetUserByEmailQueryResult(
                errors=[ErrorUtils.create_user_not_found_error(request.email)]
            )
        
        user = UserConverter.to_domain(user_dbo)
        return GetUserByEmailQueryResult(user=user)
