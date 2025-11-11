# Import config first to set up database path
from config.config import Config

from sqlalchemy import func
from src.public.tables import (
    Business, BusinessSize, AppUser, BusinessUser, BusinessUserPermissionRole,
    Cause, BusinessCausePreference, CausePreferenceRank
)
from src.analytics.tables import RegistrationStep, RegistrationInteraction
from database.db_manager import DatabaseManager
from converters.business_converter import BusinessConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from codegen.business.business_pb2 import (
    GetBusinessRequest, GetBusinessResponse,
    CreateBusinessRequest, CreateBusinessResponse,
    Business as ProtoBusiness
)
from codegen.business.business_pb2_grpc import BusinessServiceServicer
import uuid
from datetime import datetime


class BusinessService(BusinessServiceServicer):
    
    def _track_registration_step(self, session, app_user_id=None, session_id=None, 
                                step_code=1, previous_step_id=None, complete=False):
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
            
            # Check if interaction already exists for this step
            existing = session.query(RegistrationInteraction).filter(
                RegistrationInteraction.session_id == session_id,
                RegistrationInteraction.registration_step_id == registration_step.registration_step_id
            ).first()
            
            if existing:
                # Update existing interaction
                if complete and not existing.step_completed_at:
                    existing.step_completed_at = datetime.utcnow()
                return existing
            
            # Create new interaction record
            interaction = RegistrationInteraction(
                app_user_id=app_user_id,
                session_id=session_id,
                registration_step_id=registration_step.registration_step_id,
                previous_step_id=previous_step_id,
                next_step_id=None,
                step_began_at=datetime.utcnow(),
                step_completed_at=datetime.utcnow() if complete else None
            )
            
            session.add(interaction)
            session.flush()
            
            print(f"Tracked registration step: {registration_step.step_name} for session {session_id}")
            return interaction
            
        except Exception as e:
            print(f"Error tracking registration step: {e}")
            return None
    
    def GetBusiness(self, request: GetBusinessRequest, context):
        response = GetBusinessResponse()
        
        try:
            if not Validator.is_not_empty(request.business_id):
                response.errors.append(ErrorHandler.invalid_parameter('business_id'))
                return response
            
            with DatabaseManager.get_session() as session:
                db_business = session.query(Business).filter(
                    Business.business_id == request.business_id
                ).first()
                
                if not db_business:
                    response.errors.append(
                        ErrorHandler.not_found('Business', request.business_id)
                    )
                    return response
                
                domain_business = BusinessConverter.to_domain(db_business)
                response.business.CopyFrom(ProtoBusiness(
                    id=domain_business.id,
                    business_name=domain_business.business_name,
                    email=domain_business.email,
                    website_url=domain_business.website_url,
                    phone_number=domain_business.phone_number,
                    location_city=domain_business.location_city,
                    location_state=domain_business.location_state,
                    ein=domain_business.ein,
                    business_description=domain_business.business_description,
                    business_size=BusinessConverter.size_to_string(domain_business.business_size)
                ))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetBusiness: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def CreateBusiness(self, request: CreateBusinessRequest, context):
        response = CreateBusinessResponse()
        
        try:
            # Extract session_id and user info from metadata
            metadata = dict(context.invocation_metadata())
            session_id = metadata.get('session-id', None)
            
            # Validate
            errors = []
            if not Validator.is_not_empty(request.business_name):
                errors.append(ErrorHandler.invalid_parameter('business_name'))
            if not Validator.is_valid_email(request.email):
                errors.append(ErrorHandler.invalid_parameter('email'))
            if not Validator.is_not_empty(request.location_city):
                errors.append(ErrorHandler.invalid_parameter('location_city'))
            if not Validator.is_not_empty(request.location_state):
                errors.append(ErrorHandler.invalid_parameter('location_state'))
            if request.business_size and not Validator.is_valid_size(request.business_size):
                errors.append(ErrorHandler.invalid_parameter('business_size'))
            
            if errors:
                response.errors.extend(errors)
                return response
            
            with DatabaseManager.get_session() as session:
                # Get user if email provided
                app_user = None
                if request.user_email:
                    app_user = session.query(AppUser).filter(
                        func.lower(AppUser.email) == func.lower(request.user_email)
                    ).first()
                
                # Track cause_selection step if causes provided
                cause_interaction = None
                if request.cause_codes and len(request.cause_codes) > 0 and session_id:
                    cause_interaction = self._track_registration_step(
                        session=session,
                        app_user_id=app_user.app_user_id if app_user else None,
                        session_id=session_id,
                        step_code=4,  # cause_selection
                        complete=True  # Mark as complete since they selected causes
                    )
                
                # Track size step if business size provided
                size_interaction = None
                if request.business_size and session_id:
                    size_interaction = self._track_registration_step(
                        session=session,
                        app_user_id=app_user.app_user_id if app_user else None,
                        session_id=session_id,
                        step_code=5,  # size
                        previous_step_id=cause_interaction.registration_interaction_id if cause_interaction else None,
                        complete=True  # Mark as complete since they selected size
                    )
                
                # Track entity_information step (main business creation)
                entity_interaction = None
                if session_id:
                    prev_step_id = size_interaction.registration_interaction_id if size_interaction else (
                        cause_interaction.registration_interaction_id if cause_interaction else None
                    )
                    entity_interaction = self._track_registration_step(
                        session=session,
                        app_user_id=app_user.app_user_id if app_user else None,
                        session_id=session_id,
                        step_code=6,  # entity_information
                        previous_step_id=prev_step_id
                    )
                
                # Check duplicates
                existing_email = session.query(Business).filter(
                    func.lower(Business.email) == func.lower(request.email)
                ).first()
                
                if existing_email:
                    response.errors.append(
                        ErrorHandler.already_exists('Business', 'email', request.email)
                    )
                    return response
                
                existing_name = session.query(Business).filter(
                    func.lower(Business.business_name) == func.lower(request.business_name)
                ).first()
                
                if existing_name:
                    response.errors.append(
                        ErrorHandler.already_exists('Business', 'name', request.business_name)
                    )
                    return response
                
                # Get business size
                size_code = BusinessConverter.size_to_code(
                    request.business_size if request.business_size else 'SMALL'
                )
                business_size = session.query(BusinessSize).filter(
                    BusinessSize.code == size_code
                ).first()
                
                # Create business
                new_business = Business(
                    business_name=request.business_name,
                    email=request.email,
                    website_url=request.website_url or None,
                    phone_number=request.phone_number or None,
                    location_city=request.location_city,
                    location_state=request.location_state,
                    ein=request.ein or None,
                    business_description=request.business_description or '',
                    business_size_id=business_size.business_size_id
                )
                
                session.add(new_business)
                session.flush()
                
                # Link user if provided
                if app_user:
                    admin_role = session.query(BusinessUserPermissionRole).filter(
                        BusinessUserPermissionRole.code == 1
                    ).first()
                    
                    if admin_role:
                        business_user = BusinessUser(
                            business_id=new_business.business_id,
                            app_user_id=app_user.app_user_id,
                            business_user_permission_role_id=admin_role.business_user_permission_role_id
                        )
                        session.add(business_user)
                
                # Create cause preferences
                if request.cause_codes:
                    default_rank = session.query(CausePreferenceRank).filter(
                        CausePreferenceRank.code == 1
                    ).first()
                    
                    for cause_code_str in request.cause_codes:
                        # Normalize cause name
                        words = cause_code_str.split('_')
                        normalized_name = ' '.join(word.capitalize() for word in words)
                        
                        # Special cases for ampersands
                        ampersand_replacements = {
                            "Events Advocacy": "Events & Advocacy",
                            "Schools Teachers": "Schools & Teachers",
                            "Health Wellbeing": "Health & Wellbeing",
                            "Droughts Fire Management": "Droughts & Fire Management"
                        }
                        
                        if normalized_name in ampersand_replacements:
                            normalized_name = ampersand_replacements[normalized_name]
                        
                        cause = session.query(Cause).filter(
                            Cause.cause_name == normalized_name
                        ).first()
                        
                        if cause and default_rank:
                            cause_pref = BusinessCausePreference(
                                business_id=new_business.business_id,
                                cause_id=cause.cause_id,
                                cause_preference_rank_id=default_rank.cause_preference_rank_id
                            )
                            session.add(cause_pref)
                
                # Complete the entity_information step
                if entity_interaction:
                    entity_interaction.step_completed_at = datetime.utcnow()
                    print(f"Registration completed for session {session_id}")
                
                # Convert to response
                domain_business = BusinessConverter.to_domain(new_business)
                response.business.CopyFrom(ProtoBusiness(
                    id=domain_business.id,
                    business_name=domain_business.business_name,
                    email=domain_business.email,
                    website_url=domain_business.website_url,
                    phone_number=domain_business.phone_number,
                    location_city=domain_business.location_city,
                    location_state=domain_business.location_state,
                    ein=domain_business.ein,
                    business_description=domain_business.business_description,
                    business_size=BusinessConverter.size_to_string(domain_business.business_size)
                ))
                
                # Add session_id to response metadata
                if session_id:
                    context.set_trailing_metadata([
                        ('session-id', str(session_id)),
                        ('registration-complete', 'true')
                    ])
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in CreateBusiness: {e}")
            import traceback
            traceback.print_exc()
        
        return response