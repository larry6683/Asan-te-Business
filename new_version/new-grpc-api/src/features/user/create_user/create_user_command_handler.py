# new_version/new-grpc-api/src/features/user/create_user/create_user_command_handler.py
import uuid
import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import path fix
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, src_path)

from database_path_fix import import_sqlalchemy_models

# Try to import SQLAlchemy models
AppUser, UserType, SQLALCHEMY_AVAILABLE = import_sqlalchemy_models()

from config.config import Config
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils
from converters.user_converter import UserConverter
from domain.user import UserType as DomainUserType

# Keep old mock functionality
from database.db_data.users import get_user_by_email, add_user, email_exists
from database.models.user import UserDbo, UserTypeCode

from .create_user_command import CreateUserCommand, CreateUserCommandResult

class CreateUserCommandHandler(
    RequestHandler[CreateUserCommand, CreateUserCommandResult]
):
    def __init__(self):
        pass

    def handle(self, request: CreateUserCommand) -> CreateUserCommandResult:
        # Check if we should use database and if SQLAlchemy is available
        try:
            use_db = Config.use_db()
        except:
            use_db = False
            
        if not use_db or not SQLALCHEMY_AVAILABLE:
            print("Using mock database (SQLAlchemy not available or not configured)")
            return self.handle_mock(request)
        
        try:
            from database.db_connection import DatabaseConnection
            with DatabaseConnection.get_session() as session:
                return self.handle_with_sqlalchemy(session, request)
        except Exception as e:
            print(f"SQLAlchemy handler failed: {e}, falling back to mock")
            return self.handle_mock(request)
    
    def handle_with_sqlalchemy(self, session: Session, request: CreateUserCommand) -> CreateUserCommandResult:
        """SQLAlchemy implementation using the new database models"""
        try:
            # Check if email already exists
            existing_user = (session.query(AppUser)
                           .filter(func.lower(AppUser.email) == func.lower(request.email))
                           .first())
            
            if existing_user:
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_email_already_exists_error(request.email)]
                )
            
            # Validate user type
            domain_user_type = UserConverter.user_type_from_string(request.user_type)
            if not domain_user_type:
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_invalid_user_type_error(request.user_type)]
                )
            
            # Get user type code and find UserType entity
            user_type_code = UserConverter.user_type_string_to_code(request.user_type)
            user_type_entity = (session.query(UserType)
                              .filter(UserType.code == user_type_code)
                              .first())
            
            if not user_type_entity:
                return CreateUserCommandResult(
                    errors=[ErrorUtils.create_invalid_user_type_error(request.user_type)]
                )
            
            # Create new user
            new_app_user = AppUser(
                user_type_id=user_type_entity.user_type_id,
                email=request.email,
                mailing_list_signup=request.mailing_list_signup
            )
            
            session.add(new_app_user)
            session.flush()  # Flush to get the ID
            
            # Convert to domain object
            user = UserConverter.to_domain(new_app_user)
            
            return CreateUserCommandResult(user=user)
            
        except Exception as e:
            session.rollback()
            return CreateUserCommandResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_with_sqlalchemy, str(e), e)]
            )
        
    def handle_mock(self, request: CreateUserCommand) -> CreateUserCommandResult:
        """Keep existing mock functionality for development"""
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
        
        # Create new user with old DBO structure
        new_user_dbo = UserDbo(
            app_user_id=str(uuid.uuid4()),
            email=request.email,
            user_type_code=UserTypeCode.from_str(request.user_type),
            mailing_list_signup=request.mailing_list_signup
        )
        
        # Add to mock database
        add_user(new_user_dbo)
        
        # Convert old DBO to domain object
        user_type_map = {
            UserTypeCode.BUSINESS: DomainUserType.BUSINESS,
            UserTypeCode.BENEFICIARY: DomainUserType.BENEFICIARY,
            UserTypeCode.CONSUMER: DomainUserType.CONSUMER
        }
        
        from domain.user import User
        user = User(
            id=new_user_dbo.app_user_id,
            email=new_user_dbo.email,
            user_type=user_type_map[new_user_dbo.user_type_code],
            mailing_list_signup=new_user_dbo.mailing_list_signup
        )
        
        return CreateUserCommandResult(user=user)