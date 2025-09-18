from psycopg import Cursor
from config.config import Config
from database.db_utils import DBUtils
import hashlib

from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils
from converters.user_converter import UserConverter

from database.db_data.users import create_user, get_user_by_email

from .create_user_command import CreateUserCommand, CreateUserCommandResult
from codegen.error.user_error_code_pb2 import UserErrorCode

class CreateUserCommandHandler(
    RequestHandler[CreateUserCommand, CreateUserCommandResult]
):
    def __init__(self):
        pass

    def handle(self, request: CreateUserCommand) -> CreateUserCommandResult:
        if not Config.use_db():
            return self.handle_mock(request)
        
        try:
            with DBUtils.get_connection() as conn:
                with conn.cursor() as cursor:
                    return self.handle_with_db(cursor, request)
        except Exception as e:
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle, str(e), e)]
            )
    
    def handle_with_db(self, cursor: Cursor, request: CreateUserCommand) -> CreateUserCommandResult:
        """
        Database implementation - to be implemented with SQLAlchemy
        """
        try:
            # Check if user already exists
            email_hash = hashlib.md5(request.user_data.email.lower().encode()).hexdigest()
            
            check_sql = """
                SELECT email
                FROM app_user
                WHERE email_hash = %(email_hash)s
            """
            
            cursor.execute(check_sql, {"email_hash": email_hash})
            
            if cursor.fetchone():
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_email_already_exists_error(request.user_data.email)]
                )
            
            # Insert new user
            insert_sql = """
                INSERT INTO app_user (email, mailing_list_signup, user_type_id)
                VALUES (
                    %(email)s, 
                    %(mailing_list_signup)s, 
                    (
                        SELECT user_type_id
                        FROM user_type
                        WHERE code = %(user_type_code)s
                    )
                )
                RETURNING app_user_id, email, (   
                    SELECT code 
                    FROM user_type 
                    WHERE user_type_id = user_type_id 
                    LIMIT 1
                )
            """
            
            # Convert user type to code
            user_type_code_map = {
                "BUSINESS": 1,
                "BENEFICIARY": 2, 
                "CONSUMER": 3
            }
            
            params = {
                "email": request.user_data.email,
                "mailing_list_signup": request.user_data.mailing_list_signup,
                "user_type_code": user_type_code_map[request.user_data.user_type.name]
            }
            
            cursor.execute(insert_sql, params)
            result = cursor.fetchone()
            
            if not result:
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_operation_failed_error(self.handle_with_db, "Failed to create user")]
                )
            
            # Convert result to domain object
            from database.models.user import UserDbo, UserTypeCode
            user_dbo = UserDbo(
                app_user_id=result[0],
                email=result[1],
                user_type_code=UserTypeCode(result[2])
            )
            
            user = UserConverter.to_domain(user_dbo)
            
            return CreateUserCommandResult(user=user)
            
        except Exception as e:
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_with_db, str(e), e)]
            )
        
    def handle_mock(self, request: CreateUserCommand) -> CreateUserCommandResult:
        # Check if user already exists
        if get_user_by_email(request.user_data.email):
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_email_already_exists_error(request.user_data.email)]
            )
        
        # Create user
        create_user_dbo = UserConverter.to_create_user_dbo(request.user_data)
        user_dbo = create_user(create_user_dbo)
        
        if not user_dbo:
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_mock, "Failed to create user")]
            )
        
        user = UserConverter.to_domain(user_dbo)
        return CreateUserCommandResult(user=user)
