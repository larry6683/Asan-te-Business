"""
Analytics Schema - Verification Tracking Model

Tracks email verification status and verification code requests per user.
One row per user, updated as verification progresses.
"""

from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

# Import the analytics Base
from .base import Base


class VerificationTracking(Base):
    """
    Tracks email verification status and attempts per user.
    
    Key features:
    - One record per user (unique constraint on app_user_id)
    - Tracks verification completion status
    - Counts verification code requests (initial + resends)
    - Records timestamps for analytics
    - Links to session_id for journey tracking
    """
    __tablename__ = 'verification_tracking'
    __table_args__ = (
        # Index on app_user_id for fast user lookups
        Index('verification_tracking_app_user_idx', 'app_user_id'),
        
        # Index on session_id for session-based queries
        Index('verification_tracking_session_idx', 'session_id'),
        
        # Partial index for incomplete verifications
        Index(
            'verification_tracking_incomplete_idx',
            'app_user_id',
            postgresql_where=Column('email_verified').is_(False)
        ),
        
        {'schema': 'analytics'}
    )
    
    # Primary key
    verification_tracking_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid()
    )
    
    # Foreign key to public.app_user (required)
    app_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('app_user.app_user_id', ondelete='CASCADE'),
        nullable=False,
        unique=True  # One verification record per user
    )
    
    # Session where verification happened
    session_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )
    
    # Verification status
    email_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    verification_completed_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True
    )
    
    # Code request tracking
    verification_codes_requested = Column(
        Integer,
        default=1,
        nullable=False
    )
    
    first_code_requested_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )
    
    last_code_requested_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )
    
    # Standard timestamps
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
        return (f"<VerificationTracking("
                f"user={str(self.app_user_id)[:8]}, "
                f"verified={self.email_verified}, "
                f"requests={self.verification_codes_requested})>")
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'verification_tracking_id': str(self.verification_tracking_id),
            'app_user_id': str(self.app_user_id),
            'session_id': str(self.session_id),
            'email_verified': self.email_verified,
            'verification_completed_at': self.verification_completed_at.isoformat() if self.verification_completed_at else None,
            'verification_codes_requested': self.verification_codes_requested,
            'first_code_requested_at': self.first_code_requested_at.isoformat() if self.first_code_requested_at else None,
            'last_code_requested_at': self.last_code_requested_at.isoformat() if self.last_code_requested_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def time_to_verify(self):
        """Calculate how long verification took"""
        if self.verification_completed_at and self.first_code_requested_at:
            return (self.verification_completed_at - self.first_code_requested_at).total_seconds()
        return None