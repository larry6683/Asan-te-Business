import uuid
from psycopg import Cursor
from config.config import Config
from database.db_utils import DBUtils

from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils
from converters.user_converter import UserConverter
from domain.user import UserType

from database.db_data.users import get_user_by_email, add_user, email_exists
from database.models.user import UserDbo, UserTypeCode

from .create_user_command import CreateUserCommand, CreateUserCommandResult

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
        # Check if email already exists
        check_sql = """
            SELECT email
            FROM app_user
            WHERE email_hash = digest(lower(%(email)s), 'md5')
        """
        check_params = {"email": request.email}
        
        try:
            cursor.execute(check_sql, check_params)
            if cursor.fetchone():
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_email_already_exists_error(request.email)]
                )
            
            # Convert user type string to code
            user_type_code = UserTypeCode.from_str(request.user_type)
            if not user_type_code:
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_invalid_user_type_error(request.user_type)]
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
                RETURNING app_user_id, 
                email, 
                (   
                    SELECT  code 
                    FROM user_type 
                    WHERE user_type_id = app_user.user_type_id 
                    LIMIT 1
                ),
                mailing_list_signup
            """
            
            insert_params = {
                "email": request.email,
                "mailing_list_signup": request.mailing_list_signup,
                "user_type_code": user_type_code.value
            }
            
            cursor.execute(insert_sql, insert_params)
            result = cursor.fetchone()
            
            if not result:
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_operation_failed_error(self.handle_with_db, "Failed to create user")]
                )
            
            # Convert result to domain object
            user_dbo = UserDbo(
                app_user_id=result[0],
                email=result[1],
                user_type_code=UserTypeCode(result[2]),
                mailing_list_signup=result[3]
            )
            
            user = UserConverter.to_domain(user_dbo)
            return CreateUserCommandResult(user=user)
            
        except Exception as e:
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_with_db, str(e), e)]
            )
        
    def handle_mock(self, request: CreateUserCommand) -> CreateUserCommandResult:
        # Check if email already exists
        if email_exists(request.email):
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_email_already_exists_error(request.email)]
            )
        
        # Convert user type string to enum
        user_type = UserConverter.user_type_from_string(request.user_type)
        if not user_type:
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_invalid_user_type_error(request.user_type)]
            )
        
        # Create new user
        new_user_dbo = UserDbo(
            app_user_id=str(uuid.uuid4()),
            email=request.email,
            user_type_code=UserTypeCode.from_str(request.user_type),
            mailing_list_signup=request.mailing_list_signup
        )
        
        # Add to mock database
        add_user(new_user_dbo)
        
        # Convert to domain object
        user = UserConverter.to_domain(new_user_dbo)
        return CreateUserCommandResult(user=user)
