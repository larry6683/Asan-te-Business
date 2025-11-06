from enum import Enum
from datetime import datetime
from typing import Optional

class RegistrationStepCode(Enum):
    """Registration step codes matching the database"""
    SIGNUP = 1
    VERIFICATION = 2
    FIRST_LOGIN = 3
    CAUSE_SELECTION = 4
    SIZE = 5
    ENTITY_INFORMATION = 6

class RegistrationStep:
    """Domain model for registration steps"""
    def __init__(self, id: str, code: int, step_name: str, 
                 step_order: int, description: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.code = code
        self.step_name = step_name
        self.step_order = step_order
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

class RegistrationInteraction:
    """Domain model for registration interactions"""
    def __init__(self, id: str, session_id: str, registration_step_id: str,
                 app_user_id: Optional[str] = None,
                 previous_step_id: Optional[str] = None,
                 next_step_id: Optional[str] = None,
                 step_began_at: Optional[datetime] = None,
                 step_completed_at: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.app_user_id = app_user_id
        self.session_id = session_id
        self.registration_step_id = registration_step_id
        self.previous_step_id = previous_step_id
        self.next_step_id = next_step_id
        self.step_began_at = step_began_at
        self.step_completed_at = step_completed_at
        self.created_at = created_at
        self.updated_at = updated_at
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate how long the user spent on this step"""
        if self.step_completed_at and self.step_began_at:
            return (self.step_completed_at - self.step_began_at).total_seconds()
        return None
    
    @property
    def is_completed(self) -> bool:
        """Check if this step interaction is completed"""
        return self.step_completed_at is not None

class RegistrationStats:
    """Domain model for registration statistics"""
    def __init__(self):
        self.total_sessions = 0
        self.completed_registrations = 0
        self.incomplete_registrations = 0
        self.completion_rate = 0.0
        self.dropoff_by_step = {}
        self.average_duration_seconds = 0.0