# Import config first to set up database path
from config.config import Config

import uuid
from datetime import datetime, timedelta, timezone 
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import aliased, joinedload
from src.analytics.tables import ( # type: ignore
    RegistrationStep as DBRegistrationStep,
    RegistrationInteraction as DBRegistrationInteraction,
    VerificationTracking as DBVerificationTracking
)
# UPDATED: Added all necessary imports for joinedload
from src.public.tables import (
    AppUser as DBAppUser,
    Business as DBBusiness,
    Beneficiary as DBBeneficiary,
    BusinessUser as DBBusinessUser,
    BeneficiaryUser as DBBeneficiaryUser,
    BusinessCausePreference as DBBusinessCausePreference,
    BeneficiaryCausePreference as DBBeneficiaryCausePreference,
    Cause as DBCause,
    UserType as DBUserType
)

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
    
    def GetAllSessions(self, request: GetAllSessionsRequest, context):
        """Get all session logs for the analytics dashboard"""
        response = GetAllSessionsResponse()
        try:
            with DatabaseManager.get_session() as session:
                # 1. Get all steps for mapping
                steps_query = session.query(DBRegistrationStep).all()
                step_map = {str(step.registration_step_id): step for step in steps_query}
                
                # 2. Get all interactions
                all_interactions = session.query(DBRegistrationInteraction).order_by(
                    DBRegistrationInteraction.session_id,
                    DBRegistrationInteraction.step_began_at
                ).all()

                if not all_interactions:
                    return response

                # 3. Process interactions into session logs
                session_logs = {}
                user_ids_to_fetch = set()

                for interaction in all_interactions:
                    session_id_str = str(interaction.session_id)
                    if session_id_str not in session_logs:
                        session_logs[session_id_str] = {
                            "session_id": session_id_str,
                            "app_user_id": None,
                            "user_email": "N/A",
                            "started_at": interaction.step_began_at,
                            "last_activity": interaction.updated_at,
                            "latest_interaction": interaction,
                            "completed_steps": set()
                        }
                    
                    log = session_logs[session_id_str]
                    log["last_activity"] = max(log["last_activity"], interaction.updated_at)
                    log["latest_interaction"] = interaction
                    
                    if interaction.step_completed_at:
                        log["completed_steps"].add(interaction.registration_step_id)

                    if interaction.app_user_id:
                        log["app_user_id"] = str(interaction.app_user_id)
                        user_ids_to_fetch.add(interaction.app_user_id)

                # 4. Bulk fetch User & Entity Details
                user_details_map = {} # user_id_str -> {type, name, size, state, website, categories}
                
                if user_ids_to_fetch:
                    # A. Fetch Emails and actual User Types
                    users = session.query(DBAppUser).options(
                        joinedload(DBAppUser.user_type)
                    ).filter(DBAppUser.app_user_id.in_(user_ids_to_fetch)).all()
                    
                    for u in users:
                        # Determine user type from DB
                        u_type = u.user_type.user_type_name if u.user_type else "Guest"
                        if "business" in u_type.lower():
                            display_type = "Business"
                        elif "profit" in u_type.lower() or "beneficiary" in u_type.lower():
                            display_type = "Non-Profit"
                        else:
                            display_type = u_type

                        user_details_map[str(u.app_user_id)] = {
                            "email": u.email, 
                            "user_type": display_type
                        }

                    # B. Fetch Business Details
                    business_data = session.query(DBBusinessUser).join(DBBusiness).options(
                        joinedload(DBBusinessUser.business).joinedload(DBBusiness.business_size),
                        joinedload(DBBusinessUser.business).joinedload(DBBusiness.cause_preferences).joinedload(DBBusinessCausePreference.cause)
                    ).filter(DBBusinessUser.app_user_id.in_(user_ids_to_fetch)).all()

                    for bu in business_data:
                        b = bu.business
                        causes = [p.cause.cause_name for p in b.cause_preferences if p.cause]
                        size = b.business_size.business_size_name if b.business_size else "Unknown"
                        
                        if str(bu.app_user_id) in user_details_map:
                            user_details_map[str(bu.app_user_id)].update({
                                "entity_name": b.business_name,
                                "entity_size": size,
                                "entity_state": b.location_state,
                                "website": b.website_url,
                                "categories": causes
                            })

                    # C. Fetch Non-Profit Details
                    beneficiary_data = session.query(DBBeneficiaryUser).join(DBBeneficiary).options(
                        joinedload(DBBeneficiaryUser.beneficiary).joinedload(DBBeneficiary.beneficiary_size),
                        joinedload(DBBeneficiaryUser.beneficiary).joinedload(DBBeneficiary.cause_preferences).joinedload(DBBeneficiaryCausePreference.cause)
                    ).filter(DBBeneficiaryUser.app_user_id.in_(user_ids_to_fetch)).all()

                    for bu in beneficiary_data:
                        b = bu.beneficiary
                        causes = [p.cause.cause_name for p in b.cause_preferences if p.cause]
                        size = b.beneficiary_size.beneficiary_size_name if b.beneficiary_size else "Unknown"
                        
                        if str(bu.app_user_id) in user_details_map:
                            user_details_map[str(bu.app_user_id)].update({
                                "entity_name": b.beneficiary_name,
                                "entity_size": size,
                                "entity_state": b.location_state,
                                "website": b.website_url,
                                "categories": causes
                            })

                # 5. Build Response
                abandonment_threshold = datetime.now(timezone.utc) - timedelta(minutes=ABANDONMENT_MINUTES)
                
                for log in session_logs.values():
                    uid = log["app_user_id"]
                    details = user_details_map.get(uid, {}) if uid else {}
                    
                    # Determine status
                    status = "In Progress"
                    latest = log["latest_interaction"]
                    step_info = step_map.get(str(latest.registration_step_id))
                    
                    if step_info and step_info.code == 6 and latest.step_completed_at:
                        status = "Completed"
                    elif log["last_activity"] < abandonment_threshold:
                        status = "Abandoned"
                        
                    duration = (log["last_activity"] - log["started_at"]).total_seconds()

                    proto_log = ProtoSessionLog(
                        session_id=log["session_id"],
                        app_user_id=uid or "",
                        user_email=details.get("email", "N/A"),
                        status=status,
                        started_at=AnalyticsConverter.datetime_to_string(log["started_at"]),
                        last_activity=AnalyticsConverter.datetime_to_string(log["last_activity"]),
                        duration_seconds=duration,
                        # New Fields
                        user_type=details.get("user_type", "Guest"),
                        entity_name=details.get("entity_name", "-"),
                        entity_size=details.get("entity_size", "-"),
                        entity_state=details.get("entity_state", "-"),
                        website=details.get("website", "-"),
                        categories=details.get("categories", [])
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
                
                # Get unique sessions - KPI Requirement: Unique Sessions Only
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