# Import config first to set up database path
from config.config import Config

import uuid
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from src.analytics.tables import (
    RegistrationStep as DBRegistrationStep,
    RegistrationInteraction as DBRegistrationInteraction
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
    RegistrationStats as ProtoRegistrationStats
)
from codegen.analytics.analytics_pb2_grpc import AnalyticsServiceServicer

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
                    step_began_at=datetime.utcnow()
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
                interaction.step_completed_at = datetime.utcnow()
                
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
                
                # Build response
                stats = ProtoRegistrationStats(
                    total_sessions=total_sessions or 0,
                    completed_registrations=completed_sessions or 0,
                    incomplete_registrations=incomplete_sessions or 0,
                    completion_rate=completion_rate,
                    average_duration_seconds=avg_duration
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
            updated_at=AnalyticsConverter.datetime_to_string(domain_interaction.updated_at)
        )