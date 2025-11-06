# Import config first to set up database path
from config.config import Config

from src.analytics.tables import RegistrationStep as DBRegistrationStep
from src.analytics.tables import RegistrationInteraction as DBRegistrationInteraction
from domain.analytics import (
    RegistrationStep, RegistrationInteraction, RegistrationStepCode, RegistrationStats
)
from datetime import datetime
from typing import Optional

class AnalyticsConverter:
    """Converter between database models and domain models for analytics"""
    
    @staticmethod
    def step_to_domain(db_step: DBRegistrationStep) -> RegistrationStep:
        """Convert database registration step to domain model"""
        return RegistrationStep(
            id=str(db_step.registration_step_id),
            code=db_step.code,
            step_name=db_step.step_name,
            step_order=db_step.step_order,
            description=db_step.description,
            created_at=db_step.created_at,
            updated_at=db_step.updated_at
        )
    
    @staticmethod
    def interaction_to_domain(db_interaction: DBRegistrationInteraction) -> RegistrationInteraction:
        """Convert database registration interaction to domain model"""
        return RegistrationInteraction(
            id=str(db_interaction.registration_interaction_id),
            app_user_id=str(db_interaction.app_user_id) if db_interaction.app_user_id else None,
            session_id=str(db_interaction.session_id),
            registration_step_id=str(db_interaction.registration_step_id),
            previous_step_id=str(db_interaction.previous_step_id) if db_interaction.previous_step_id else None,
            next_step_id=str(db_interaction.next_step_id) if db_interaction.next_step_id else None,
            step_began_at=db_interaction.step_began_at,
            step_completed_at=db_interaction.step_completed_at,
            created_at=db_interaction.created_at,
            updated_at=db_interaction.updated_at
        )
    
    @staticmethod
    def datetime_to_string(dt: Optional[datetime]) -> str:
        """Convert datetime to ISO format string"""
        if dt:
            return dt.isoformat()
        return ""
    
    @staticmethod
    def string_to_datetime(dt_str: str) -> Optional[datetime]:
        """Convert ISO format string to datetime"""
        if dt_str:
            try:
                return datetime.fromisoformat(dt_str)
            except:
                return None
        return None
    
    @staticmethod
    def code_to_step_name(code: int) -> str:
        """Map step code to step name"""
        step_map = {
            1: "signup",
            2: "verification",
            3: "first_login",
            4: "cause_selection",
            5: "size",
            6: "entity_information"
        }
        return step_map.get(code, "unknown")