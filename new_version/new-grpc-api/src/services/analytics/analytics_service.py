# Import config first to set up database path
from config.config import Config

import uuid
# --- CORRECTED IMPORT ---
from datetime import datetime, timedelta, timezone 
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import aliased
from src.analytics.tables import ( # type: ignore
    RegistrationStep as DBRegistrationStep,
    RegistrationInteraction as DBRegistrationInteraction,
    VerificationTracking as DBVerificationTracking
)
# UPDATE THIS IMPORT
from src.public.tables import (
    AppUser as DBAppUser,
    Business as DBBusiness,
    Beneficiary as DBBeneficiary
)
from src.public.tables import AppUser as DBAppUser 

from database.db_manager import DatabaseManager
from converters.analytics_converter import AnalyticsConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from codegen.analytics.analytics_pb2 import (
    TrackStepRequest, TrackStepResponse,
    CompleteStepRequest, CompleteStepResponse,
    GetRegistrationStepsRequest, GetRegistrationStepsResponse,
    GetUserJourneyRequest, GetUserJourneyResponse,
    GetSessionJourneyRequest, GetSessionJourneyResponse,
    GetRegistrationStatsRequest, GetRegistrationStatsResponse,
    RegistrationStep as ProtoRegistrationStep,
    RegistrationInteraction as ProtoRegistrationInteraction,
    RegistrationStats as ProtoRegistrationStats,
    TrackVerificationRequestRequest, TrackVerificationRequestResponse,
    MarkVerificationCompleteRequest, MarkVerificationCompleteResponse,
    GetVerificationStatusRequest, GetVerificationStatusResponse,
    VerificationTracking as ProtoVerificationTracking,
    GetAllSessionsRequest, GetAllSessionsResponse,
    SessionLog as ProtoSessionLog
)
from codegen.analytics.analytics_pb2_grpc import AnalyticsServiceServicer

ABANDONMENT_MINUTES = 30

class AnalyticsService(AnalyticsServiceServicer):
    """Analytics service implementation for tracking registration workflows"""
    
    def TrackStep(self, request: TrackStepRequest, context):
        """Track a registration step interaction"""
        response = TrackStepResponse()
        
        try:
            # Validate
            errors = []
            if not Validator.is_not_empty(request.session_id):
                errors.append(ErrorHandler.invalid_parameter('session_id'))
            if request.step_code < 1 or request.step_code > 6:
                errors.append(ErrorHandler.invalid_parameter('step_code'))
            
            if errors:
                response.errors.extend(errors)
                return response
            
            with DatabaseManager.get_session() as session:
                # Get the registration step
                registration_step = session.query(DBRegistrationStep).filter(
                    DBRegistrationStep.code == request.step_code
                ).first()
                
                if not registration_step:
                    response.errors.append(
                        ErrorHandler.not_found('RegistrationStep', str(request.step_code))
                    )
                    return response
                
                # Get previous step if provided
                previous_step_id = None
                if request.previous_step_code > 0:
                    previous_step = session.query(DBRegistrationStep).filter(
                        DBRegistrationStep.code == request.previous_step_code
                    ).first()
                    if previous_step:
                        previous_step_id = previous_step.registration_step_id
                
                # Get next step if provided
                next_step_id = None
                if request.next_step_code > 0:
                    next_step = session.query(DBRegistrationStep).filter(
                        DBRegistrationStep.code == request.next_step_code
                    ).first()
                    if next_step:
                        next_step_id = next_step.registration_step_id
                
                # Parse session_id as UUID
                try:
                    session_uuid = uuid.UUID(request.session_id)
                except ValueError:
                    response.errors.append(
                        ErrorHandler.invalid_parameter('session_id must be a valid UUID')
                    )
                    return response
                
                # Parse app_user_id if provided
                app_user_uuid = None
                if request.app_user_id:
                    try:
                        app_user_uuid = uuid.UUID(request.app_user_id)
                    except ValueError:
                        # It's OK if app_user_id is not valid - anonymous tracking
                        pass
                
                # Create the interaction
                new_interaction = DBRegistrationInteraction(
                    app_user_id=app_user_uuid,
                    session_id=session_uuid,
                    registration_step_id=registration_step.registration_step_id,
                    previous_step_id=previous_step_id,
                    next_step_id=next_step_id,
                    # --- FIXED ---
                    step_began_at=datetime.now(timezone.utc)
                )
                
                session.add(new_interaction)
                session.flush()
                
                # Convert to domain and proto
                domain_interaction = AnalyticsConverter.interaction_to_domain(new_interaction)
                response.interaction.CopyFrom(self._interaction_to_proto(domain_interaction))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in TrackStep: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def CompleteStep(self, request: CompleteStepRequest, context):
        """Mark a step as completed"""
        response = CompleteStepResponse()
        
        try:
            if not Validator.is_not_empty(request.interaction_id):
                response.errors.append(ErrorHandler.invalid_parameter('interaction_id'))
                return response
            
            with DatabaseManager.get_session() as session:
                # Get the interaction
                interaction = session.query(DBRegistrationInteraction).filter(
                    DBRegistrationInteraction.registration_interaction_id == request.interaction_id
                ).first()
                
                if not interaction:
                    response.errors.append(
                        ErrorHandler.not_found('RegistrationInteraction', request.interaction_id)
                    )
                    return response
                
                # Update completion time
                # --- FIXED ---
                interaction.step_completed_at = datetime.now(timezone.utc)
                
                # Update next_step_id if provided
                if request.next_step_code > 0:
                    next_step = session.query(DBRegistrationStep).filter(
                        DBRegistrationStep.code == request.next_step_code
                    ).first()
                    if next_step:
                        interaction.next_step_id = next_step.registration_step_id
                
                session.flush()
                
                # Convert to response
                domain_interaction = AnalyticsConverter.interaction_to_domain(interaction)
                response.interaction.CopyFrom(self._interaction_to_proto(domain_interaction))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in CompleteStep: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    # ---
    # NEW METHOD: GetAllSessions
    # ---
    def GetAllSessions(self, request: GetAllSessionsRequest, context):
        """Get all session logs for the analytics dashboard"""
        response = GetAllSessionsResponse()
        try:
            with DatabaseManager.get_session() as session:
                # 1. Get all steps for mapping
                steps_query = session.query(DBRegistrationStep).all()
                step_map = {str(step.registration_step_id): step for step in steps_query}
                
                # 2. Get all user IDs and emails for mapping
                users_query = session.query(DBAppUser.app_user_id, DBAppUser.email).all()
                user_email_map = {str(user.app_user_id): user.email for user in users_query}

                # 3. Get all interactions, ordered by session and time
                all_interactions = session.query(DBRegistrationInteraction).order_by(
                    DBRegistrationInteraction.session_id,
                    DBRegistrationInteraction.step_began_at
                ).all()

                if not all_interactions:
                    return response # Return empty response if no data

                # 4. Process interactions into session logs in Python
                session_logs = {}
                for interaction in all_interactions:
                    session_id_str = str(interaction.session_id)
                    if session_id_str not in session_logs:
                        # Initialize new session log
                        session_logs[session_id_str] = {
                            "session_id": session_id_str,
                            "app_user_id": str(interaction.app_user_id) if interaction.app_user_id else None,
                            "user_email": user_email_map.get(str(interaction.app_user_id)),
                            "started_at": interaction.step_began_at,
                            "last_activity": interaction.updated_at,
                            "latest_interaction": interaction,
                            "completed_step_ids": set()
                        }
                    
                    # Update session log with this interaction's data
                    log = session_logs[session_id_str]
                    log["last_activity"] = max(log["last_activity"], interaction.updated_at)
                    log["latest_interaction"] = interaction # This one is the latest so far
                    
                    if interaction.app_user_id and not log["app_user_id"]:
                         log["app_user_id"] = str(interaction.app_user_id)
                         log["user_email"] = user_email_map.get(str(interaction.app_user_id))

                    if interaction.step_completed_at:
                        log["completed_step_ids"].add(str(interaction.registration_step_id))

                # 5. Convert processed logs into Proto messages
                # --- FIXED: This is the line that caused the error ---
                abandonment_threshold = datetime.now(timezone.utc) - timedelta(minutes=ABANDONMENT_MINUTES)
                
                for log in session_logs.values():
                    latest_interaction = log["latest_interaction"]
                    current_step_db = step_map.get(str(latest_interaction.registration_step_id))
                    
                    if not current_step_db:
                        continue # Skip if step not found

                    # Determine final state
                    status = "In Progress"
                    if current_step_db.code == 6 and latest_interaction.step_completed_at:
                        status = "Completed"
                    # This comparison is now safe
                    elif log["last_activity"] < abandonment_threshold:
                        status = "Abandoned"

                    duration = (log["last_activity"] - log["started_at"]).total_seconds()
                    
                    proto_log = ProtoSessionLog(
                        session_id=log["session_id"],
                        app_user_id=log["app_user_id"] or "",
                        user_email=log["user_email"] or "N/A",
                        status=status,
                        current_step_code=current_step_db.code,
                        current_step_name=current_step_db.step_name,
                        steps_completed=len(log["completed_step_ids"]),
                        started_at=AnalyticsConverter.datetime_to_string(log["started_at"]),
                        last_activity=AnalyticsConverter.datetime_to_string(log["last_activity"]),
                        duration_seconds=duration
                    )
                    response.sessions.append(proto_log)

        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetAllSessions: {e}")
            import traceback
            traceback.print_exc()
            
        return response

    
    def GetRegistrationSteps(self, request: GetRegistrationStepsRequest, context):
        """Get all registration steps"""
        response = GetRegistrationStepsResponse()
        
        try:
            with DatabaseManager.get_session() as session:
                steps = session.query(DBRegistrationStep).order_by(
                    DBRegistrationStep.step_order
                ).all()
                
                for db_step in steps:
                    domain_step = AnalyticsConverter.step_to_domain(db_step)
                    proto_step = ProtoRegistrationStep(
                        id=domain_step.id,
                        code=domain_step.code,
                        step_name=domain_step.step_name,
                        step_order=domain_step.step_order,
                        description=domain_step.description,
                        created_at=AnalyticsConverter.datetime_to_string(domain_step.created_at),
                        updated_at=AnalyticsConverter.datetime_to_string(domain_step.updated_at)
                    )
                    response.steps.append(proto_step)
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetRegistrationSteps: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def GetUserJourney(self, request: GetUserJourneyRequest, context):
        """Get user's registration journey"""
        response = GetUserJourneyResponse()
        
        try:
            if not Validator.is_not_empty(request.app_user_id):
                response.errors.append(ErrorHandler.invalid_parameter('app_user_id'))
                return response
            
            with DatabaseManager.get_session() as session:
                interactions = session.query(DBRegistrationInteraction).filter(
                    DBRegistrationInteraction.app_user_id == request.app_user_id
                ).order_by(
                    DBRegistrationInteraction.step_began_at
                ).all()
                
                for db_interaction in interactions:
                    domain_interaction = AnalyticsConverter.interaction_to_domain(db_interaction)
                    response.interactions.append(self._interaction_to_proto(domain_interaction))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetUserJourney: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def GetSessionJourney(self, request: GetSessionJourneyRequest, context):
        """Get session's registration journey"""
        response = GetSessionJourneyResponse()
        
        try:
            if not Validator.is_not_empty(request.session_id):
                response.errors.append(ErrorHandler.invalid_parameter('session_id'))
                return response
            
            # Parse session_id as UUID
            try:
                session_uuid = uuid.UUID(request.session_id)
            except ValueError:
                response.errors.append(
                    ErrorHandler.invalid_parameter('session_id must be a valid UUID')
                )
                return response
            
            with DatabaseManager.get_session() as session:
                interactions = session.query(DBRegistrationInteraction).filter(
                    DBRegistrationInteraction.session_id == session_uuid
                ).order_by(
                    DBRegistrationInteraction.step_began_at
                ).all()
                
                for db_interaction in interactions:
                    domain_interaction = AnalyticsConverter.interaction_to_domain(db_interaction)
                    response.interactions.append(self._interaction_to_proto(domain_interaction))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetSessionJourney: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def GetRegistrationStats(self, request: GetRegistrationStatsRequest, context):
        """Get registration statistics"""
        response = GetRegistrationStatsResponse()
        
        try:
            with DatabaseManager.get_session() as session:
                # Parse dates if provided
                start_date = None
                end_date = None
                if request.start_date:
                    start_date = AnalyticsConverter.string_to_datetime(request.start_date)
                if request.end_date:
                    end_date = AnalyticsConverter.string_to_datetime(request.end_date)
                
                # Build base query
                query = session.query(DBRegistrationInteraction)
                if start_date:
                    query = query.filter(DBRegistrationInteraction.step_began_at >= start_date)
                if end_date:
                    query = query.filter(DBRegistrationInteraction.step_began_at <= end_date)
                
                # Get unique sessions
                total_sessions = query.with_entities(
                    func.count(func.distinct(DBRegistrationInteraction.session_id))
                ).scalar()
                
                # Get completed registrations (sessions that reached step 6)
                step_6 = session.query(DBRegistrationStep).filter(
                    DBRegistrationStep.code == 6
                ).first()
                
                if step_6:
                    completed_query = query.filter(
                        DBRegistrationInteraction.registration_step_id == step_6.registration_step_id,
                        DBRegistrationInteraction.step_completed_at.isnot(None)
                    )
                    completed_sessions = completed_query.with_entities(
                        func.count(func.distinct(DBRegistrationInteraction.session_id))
                    ).scalar()
                else:
                    completed_sessions = 0
                
                incomplete_sessions = total_sessions - completed_sessions
                
                # Calculate completion rate
                completion_rate = 0.0
                if total_sessions > 0:
                    completion_rate = (completed_sessions / total_sessions) * 100
                
                # Calculate dropoff by step
                all_steps = session.query(DBRegistrationStep).order_by(
                    DBRegistrationStep.step_order
                ).all()
                
                dropoff_by_step = {}
                for step in all_steps:
                    incomplete_at_step = query.filter(
                        DBRegistrationInteraction.registration_step_id == step.registration_step_id,
                        DBRegistrationInteraction.step_completed_at.is_(None)
                    ).count()
                    dropoff_by_step[step.step_name] = incomplete_at_step
                
                # Calculate average duration for completed interactions
                completed_interactions = query.filter(
                    DBRegistrationInteraction.step_completed_at.isnot(None)
                ).all()
                
                total_duration = 0.0
                count = 0
                for interaction in completed_interactions:
                    if interaction.step_began_at and interaction.step_completed_at:
                        duration = (interaction.step_completed_at - interaction.step_began_at).total_seconds()
                        total_duration += duration
                        count += 1
                
                avg_duration = total_duration / count if count > 0 else 0.0
                
                # --- NEW KPI QUERIES ---
                # Get total users from app_user table
                total_users = session.query(func.count(DBAppUser.app_user_id)).scalar() or 0
                
                # Get total businesses from business table
                total_businesses = session.query(func.count(DBBusiness.business_id)).scalar() or 0
                
                # Get total non-profits from beneficiary table
                total_non_profits = session.query(func.count(DBBeneficiary.beneficiary_id)).scalar() or 0

                # Build response with new fields
                stats = ProtoRegistrationStats(
                    total_sessions=total_sessions or 0,
                    completed_registrations=completed_sessions or 0,
                    incomplete_registrations=incomplete_sessions or 0,
                    completion_rate=completion_rate,
                    average_duration_seconds=avg_duration,
                    # Add new fields here
                    total_users=total_users,
                    total_businesses=total_businesses,
                    total_non_profits=total_non_profits
                )
                
                # Add dropoff_by_step to the map
                for step_name, count in dropoff_by_step.items():
                    stats.dropoff_by_step[step_name] = count
                
                response.stats.CopyFrom(stats)
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetRegistrationStats: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def _interaction_to_proto(self, domain_interaction) -> ProtoRegistrationInteraction:
        """Convert domain interaction to proto"""
        return ProtoRegistrationInteraction(
            id=domain_interaction.id,
            app_user_id=domain_interaction.app_user_id or "",
            session_id=domain_interaction.session_id,
            registration_step_id=domain_interaction.registration_step_id,
            previous_step_id=domain_interaction.previous_step_id or "",
            next_step_id=domain_interaction.next_step_id or "",
            step_began_at=AnalyticsConverter.datetime_to_string(domain_interaction.step_began_at),
            step_completed_at=AnalyticsConverter.datetime_to_string(domain_interaction.step_completed_at),
            created_at=AnalyticsConverter.datetime_to_string(domain_interaction.created_at),
            updated_at=AnalyticsConverter.datetime_to_string(domain_interaction.updated_at))

    
    def TrackVerificationRequest(self, request: TrackVerificationRequestRequest, context):
        """Track verification code request (initial or resend)"""
        response = TrackVerificationRequestResponse()
        
        try:
            # Validate
            if not Validator.is_not_empty(request.app_user_id):
                response.errors.append(ErrorHandler.invalid_parameter('app_user_id'))
                return response
            if not Validator.is_not_empty(request.session_id):
                response.errors.append(ErrorHandler.invalid_parameter('session_id'))
                return response
            
            # Parse UUIDs
            try:
                app_user_uuid = uuid.UUID(request.app_user_id)
                session_uuid = uuid.UUID(request.session_id)
            except ValueError:
                response.errors.append(ErrorHandler.invalid_parameter('Invalid UUID format'))
                return response
            
            with DatabaseManager.get_session() as session:
                # Check if record exists
                vt = session.query(DBVerificationTracking).filter(
                    DBVerificationTracking.app_user_id == app_user_uuid
                ).first()
                
                if vt:
                    # Existing record - increment count
                    vt.verification_codes_requested += 1
                    # --- FIXED ---
                    vt.last_code_requested_at = datetime.now(timezone.utc)
                    print(f"📧 Verification resend #{vt.verification_codes_requested} for user {request.app_user_id}")
                else:
                    # New record - first request
                    vt = DBVerificationTracking(
                        app_user_id=app_user_uuid,
                        session_id=session_uuid,
                        verification_codes_requested=1,
                        email_verified=False
                    )
                    session.add(vt)
                    print(f"📧 Initial verification request for user {request.app_user_id}")
                
                session.flush()
                
                # Convert to proto
                response.verification_tracking.CopyFrom(self._verification_to_proto(vt))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in TrackVerificationRequest: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def MarkVerificationComplete(self, request: MarkVerificationCompleteRequest, context):
        """Mark email verification as complete"""
        response = MarkVerificationCompleteResponse()
        
        try:
            # Validate
            if not Validator.is_not_empty(request.app_user_id):
                response.errors.append(ErrorHandler.invalid_parameter('app_user_id'))
                return response
            
            # Parse UUID
            try:
                app_user_uuid = uuid.UUID(request.app_user_id)
            except ValueError:
                response.errors.append(ErrorHandler.invalid_parameter('Invalid UUID format'))
                return response
            
            with DatabaseManager.get_session() as session:
                vt = session.query(DBVerificationTracking).filter(
                    DBVerificationTracking.app_user_id == app_user_uuid
                ).first()
                
                if vt:
                    vt.email_verified = True
                    # --- FIXED ---
                    vt.verification_completed_at = datetime.now(timezone.utc)
                    session.flush()
                    print(f"✅ Verification completed for user {request.app_user_id}")
                    response.verification_tracking.CopyFrom(self._verification_to_proto(vt))
                else:
                    # Create record if doesn't exist
                    session_uuid = uuid.UUID(request.session_id) if request.session_id else None
                    vt = DBVerificationTracking(
                        app_user_id=app_user_uuid,
                        session_id=session_uuid,
                        verification_codes_requested=1,
                        email_verified=True,
                        # --- FIXED ---
                        verification_completed_at=datetime.now(timezone.utc)
                    )
                    session.add(vt)
                    session.flush()
                    print(f"✅ Verification completed (created record) for user {request.app_user_id}")
                    response.verification_tracking.CopyFrom(self._verification_to_proto(vt))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in MarkVerificationComplete: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def GetVerificationStatus(self, request: GetVerificationStatusRequest, context):
        """Get verification status for a user"""
        response = GetVerificationStatusResponse()
        
        try:
            if not Validator.is_not_empty(request.app_user_id):
                response.errors.append(ErrorHandler.invalid_parameter('app_user_id'))
                return response
            
            try:
                app_user_uuid = uuid.UUID(request.app_user_id)
            except ValueError:
                response.errors.append(ErrorHandler.invalid_parameter('Invalid UUID format'))
                return response
            
            with DatabaseManager.get_session() as session:
                vt = session.query(DBVerificationTracking).filter(
                    DBVerificationTracking.app_user_id == app_user_uuid
                ).first()
                
                if vt:
                    response.verification_tracking.CopyFrom(self._verification_to_proto(vt))
                else:
                    response.errors.append(
                        ErrorHandler.not_found('VerificationTracking', request.app_user_id)
                    )
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetVerificationStatus: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def _verification_to_proto(self, db_verification) -> ProtoVerificationTracking:
        """Convert DB verification to proto"""
        return ProtoVerificationTracking(
            id=str(db_verification.verification_tracking_id),
            app_user_id=str(db_verification.app_user_id),
            session_id=str(db_verification.session_id),
            email_verified=db_verification.email_verified,
            verification_completed_at=AnalyticsConverter.datetime_to_string(db_verification.verification_completed_at),
            verification_codes_requested=db_verification.verification_codes_requested,
            first_code_requested_at=AnalyticsConverter.datetime_to_string(db_verification.first_code_requested_at),
            last_code_requested_at=AnalyticsConverter.datetime_to_string(db_verification.last_code_requested_at),
            created_at=AnalyticsConverter.datetime_to_string(db_verification.created_at),
            updated_at=AnalyticsConverter.datetime_to_string(db_verification.updated_at)
        )