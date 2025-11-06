# Import config first to set up database path
from config.config import Config

from sqlalchemy import func
from src.public.tables import AppUser, UserType
from database.db_manager import DatabaseManager
from converters.user_converter import UserConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from codegen.user.user_pb2 import (
    GetUserRequest, GetUserResponse,
    CreateUserRequest, CreateUserResponse,
    User as ProtoUser
)
from codegen.user.user_pb2_grpc import UserServiceServicer

class UserService(UserServiceServicer):
    
    def GetUser(self, request: GetUserRequest, context):
        response = GetUserResponse()
        
        try:
            # Validate
            if not Validator.is_valid_email(request.email):
                response.errors.append(ErrorHandler.invalid_parameter('email'))
                return response
            
            # Query database
            with DatabaseManager.get_session() as session:
                db_user = session.query(AppUser).join(UserType).filter(
                    func.lower(AppUser.email) == func.lower(request.email)
                ).first()
                
                if not db_user:
                    response.errors.append(
                        ErrorHandler.not_found('User', request.email)
                    )
                    return response
                
                # Convert to domain and proto
                domain_user = UserConverter.to_domain(db_user)
                response.user.CopyFrom(ProtoUser(
                    id=domain_user.id,
                    email=domain_user.email,
                    user_type=UserConverter.user_type_to_string(domain_user.user_type),
                    mailing_list_signup=domain_user.mailing_list_signup
                ))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetUser: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def CreateUser(self, request: CreateUserRequest, context):
        response = CreateUserResponse()
        
        try:
            # Validate
            if not Validator.is_valid_email(request.email):
                response.errors.append(ErrorHandler.invalid_parameter('email'))
                return response
            
            if not Validator.is_valid_user_type(request.user_type):
                response.errors.append(ErrorHandler.invalid_parameter('user_type'))
                return response
            
            with DatabaseManager.get_session() as session:
                # Check if user exists
                existing = session.query(AppUser).filter(
                    func.lower(AppUser.email) == func.lower(request.email)
                ).first()
                
                if existing:
                    response.errors.append(
                        ErrorHandler.already_exists('User', 'email', request.email)
                    )
                    return response
                
                # Get user type entity
                user_type_code = UserConverter.user_type_to_code(request.user_type)
                user_type = session.query(UserType).filter(
                    UserType.code == user_type_code
                ).first()
                
                # Create user
                new_user = AppUser(
                    email=request.email,
                    user_type_id=user_type.user_type_id,
                    mailing_list_signup=request.mailing_list_signup
                )
                
                session.add(new_user)
                session.flush()
                
                # Convert to domain and proto
                domain_user = UserConverter.to_domain(new_user)
                response.user.CopyFrom(ProtoUser(
                    id=domain_user.id,
                    email=domain_user.email,
                    user_type=UserConverter.user_type_to_string(domain_user.user_type),
                    mailing_list_signup=domain_user.mailing_list_signup
                ))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in CreateUser: {e}")
            import traceback
            traceback.print_exc()
        
        return response
