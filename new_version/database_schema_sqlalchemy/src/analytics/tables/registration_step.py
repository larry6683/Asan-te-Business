"""
Analytics Schema - Registration Step Model

Defines the 6 system-level registration steps that users progress through.
This is a reference/lookup table that should be populated once and rarely changed.
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

import uuid
from .base import Base


class RegistrationStep(Base):
    """
    System-defined registration steps that users progress through.
    
    Steps defined in CU Boulder spec:
    1. signup - Creates session_id, first API request with user_id = NULL
    2. verification - Email verification step
    3. first_login - First authenticated request with email
    4. cause_selection - User selects causes/preferences
    5. size - Organization size selection
    6. entity_information - Final registration details
    """
    __tablename__ = 'registration_step'
    __table_args__ = (
        Index('registration_step_code_idx', 'code'),
        {'schema': 'analytics'}
    )
    
    # Primary key
    registration_step_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid()
    )
    
    # Unique code for each step (1-6)
    code = Column(Integer, unique=True, nullable=False)
    
    # Human-readable step name
    step_name = Column(Text, nullable=False)
    
    # Order in the registration flow
    step_order = Column(Integer, nullable=False)
    
    # Detailed description of what happens in this step
    description = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
    
    def __repr__(self):
        return f"<RegistrationStep(code={self.code}, name='{self.step_name}', order={self.step_order})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'registration_step_id': str(self.registration_step_id),
            'code': self.code,
            'step_name': self.step_name,
            'step_order': self.step_order,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Predefined steps from spec
REGISTRATION_STEPS = [
    {
        'code': 1,
        'step_name': 'signup',
        'step_order': 1,
        'description': 'Creates a session_id, stores it in local storage, sends first API request with user_id = NULL.'
    },
    {
        'code': 2,
        'step_name': 'verification',
        'step_order': 2,
        'description': 'Reuses existing session_id. Tracks verification step completion.'
    },
    {
        'code': 3,
        'step_name': 'first_login',
        'step_order': 3,
        'description': 'Sends an API request including email after user creation, with session_id.'
    },
    {
        'code': 4,
        'step_name': 'cause_selection',
        'step_order': 4,
        'description': 'Captures cause preference step.'
    },
    {
        'code': 5,
        'step_name': 'size',
        'step_order': 5,
        'description': 'Captures organization size input.'
    },
    {
        'code': 6,
        'step_name': 'entity_information',
        'step_order': 6,
        'description': 'Final registration step collecting organization details.'
    }
]