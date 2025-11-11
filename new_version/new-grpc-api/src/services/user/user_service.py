# Import config first to set up database path
from config.config import Config

from sqlalchemy import func
from src.public.tables import AppUser, UserType
from src.analytics.tables import RegistrationStep, RegistrationInteraction
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
import uuid
from datetime import datetime


class UserService(UserServiceServicer):
    
    def _track_registration_step(self, session, app_user_id=None, session_id=None, 
                                step_code=1, previous_step_id=None):
        """Helper method to track registration interactions"""
        try:
            # Get the registration step
            registration_step = session.query(RegistrationStep).filter(
                RegistrationStep.code == step_code
            ).first()
            
            if not registration_step:
                print(f"Warning: Registration step {step_code} not found")
                return None
            
            # Ensure session_id is a UUID
            if session_id and isinstance(session_id, str):
                try:
                    session_id = uuid.UUID(session_id)
                except ValueError:
                    session_id = uuid.uuid4()
            elif not session_id:
                session_id = uuid.uuid4()
            
            # Create interaction record
            interaction = RegistrationInteraction(
                app_user_id=app_user_id,
                session_id=session_id,
                registration_step_id=registration_step.registration_step_id,
                previous_step_id=previous_step_id,
                next_step_id=None,
                step_began_at=datetime.utcnow(),
                step_completed_at=None
            )
            
            session.add(interaction)
            session.flush()
            
            print(f"Tracked registration step: {registration_step.step_name} for session {session_id}")
            return interaction
            
        except Exception as e:
            print(f"Error tracking registration step: {e}")
            return None
    
    def GetUser(self, request: GetUserRequest, context):
        response = GetUserResponse()
        
        try:
            # Extract session_id from metadata if available
            metadata = dict(context.invocation_metadata())
            session_id = metadata.get('session-id', None)
            
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
                
                # Track first_login step if this is part of registration flow
                if session_id:
                    self._track_registration_step(
                        session=session,
                        app_user_id=db_user.app_user_id,
                        session_id=session_id,
                        step_code=3  # first_login
                    )
                
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
            # Extract session_id from metadata if available
            metadata = dict(context.invocation_metadata())
            session_id = metadata.get('session-id', None)
            
            # Validate
            if not Validator.is_valid_email(request.email):
                response.errors.append(ErrorHandler.invalid_parameter('email'))
                return response
            
            if not Validator.is_valid_user_type(request.user_type):
                response.errors.append(ErrorHandler.invalid_parameter('user_type'))
                return response
            
            with DatabaseManager.get_session() as session:
                # Track signup step (before user exists)
                signup_interaction = None
                if session_id:
                    signup_interaction = self._track_registration_step(
                        session=session,
                        app_user_id=None,  # No user yet
                        session_id=session_id,
                        step_code=1  # signup
                    )
                
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
                
                # Complete signup step and update with user_id
                if signup_interaction:
                    signup_interaction.app_user_id = new_user.app_user_id
                    signup_interaction.step_completed_at = datetime.utcnow()
                    
                    # Track verification step (immediately after signup)
                    self._track_registration_step(
                        session=session,
                        app_user_id=new_user.app_user_id,
                        session_id=session_id,
                        step_code=2,  # verification
                        previous_step_id=signup_interaction.registration_interaction_id
                    )
                
                # Convert to domain and proto
                domain_user = UserConverter.to_domain(new_user)
                response.user.CopyFrom(ProtoUser(
                    id=domain_user.id,
                    email=domain_user.email,
                    user_type=UserConverter.user_type_to_string(domain_user.user_type),
                    mailing_list_signup=domain_user.mailing_list_signup
                ))
                
                # Add session_id to response metadata for frontend tracking
                if session_id:
                    context.set_trailing_metadata([
                        ('session-id', str(session_id))
                    ])
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in CreateUser: {e}")
            import traceback
            traceback.print_exc()
        
        return response