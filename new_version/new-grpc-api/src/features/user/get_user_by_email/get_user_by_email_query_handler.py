# new_version/new-grpc-api/src/features/user/get_user_by_email/get_user_by_email_query_handler.py
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

# Keep old mock functionality
from database.db_data.users import get_user_by_email

from .get_user_by_email_query import GetUserByEmailQuery, GetUserByEmailQueryResult

class GetUserByEmailQueryHandler(
    RequestHandler[GetUserByEmailQuery, GetUserByEmailQueryResult]
):
    def __init__(self):
        pass

    def handle(self, request: GetUserByEmailQuery) -> GetUserByEmailQueryResult:
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
    
    def handle_with_sqlalchemy(self, session: Session, request: GetUserByEmailQuery) -> GetUserByEmailQueryResult:
        """SQLAlchemy implementation using the new database models"""
        try:
            # Query user by email with join to user_type
            app_user = (session.query(AppUser)
                       .join(UserType)
                       .filter(func.lower(AppUser.email) == func.lower(request.email))
                       .first())
            
            if not app_user:
                return GetUserByEmailQueryResult(
                    errors=[ErrorUtils.create_user_not_found_error(request.email)]
                )
            
            # Convert to domain object
            user = UserConverter.to_domain(app_user)
            
            return GetUserByEmailQueryResult(user=user)
            
        except Exception as e:
            return GetUserByEmailQueryResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_with_sqlalchemy, str(e), e)]
            )
        
    def handle_mock(self, request: GetUserByEmailQuery) -> GetUserByEmailQueryResult:
        """Keep existing mock functionality for development"""
        user_dbo = get_user_by_email(request.email)
        
        if not user_dbo:
            return GetUserByEmailQueryResult(
                errors=[ErrorUtils.create_user_not_found_error(request.email)]
            )
        
        # Convert old DBO to domain
        from domain.user import User, UserType as DomainUserType
        from database.models.user import UserTypeCode
        
        # Map old UserTypeCode to domain UserType
        user_type_map = {
            UserTypeCode.BUSINESS: DomainUserType.BUSINESS,
            UserTypeCode.BENEFICIARY: DomainUserType.BENEFICIARY,
            UserTypeCode.CONSUMER: DomainUserType.CONSUMER
        }
        
        user = User(
            id=user_dbo.app_user_id,
            email=user_dbo.email,
            user_type=user_type_map[user_dbo.user_type_code],
            mailing_list_signup=user_dbo.mailing_list_signup
        )
        
        return GetUserByEmailQueryResult(user=user)