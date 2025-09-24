from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BusinessCausePreference(Base):
    __tablename__ = 'business_cause_preference'
    
    business_cause_preference_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    business_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business.business_id'),
        nullable=False
    )
    
    cause_id = Column(
        UUID(as_uuid=True),
        ForeignKey('cause.cause_id'),
        nullable=False
    )
    
    cause_preference_rank_id = Column(
        UUID(as_uuid=True),
        ForeignKey('cause_preference_rank.cause_preference_rank_id'),
        nullable=False
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=func.now()
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )
    
    business = relationship("Business", back_populates="cause_preferences")
    cause = relationship("Cause", back_populates="business_preferences")
    preference_rank = relationship("CausePreferenceRank", back_populates="business_preferences")
    
    def __repr__(self):
        return f"<BusinessCausePreference(business_id='{self.business_id}', cause_id='{self.cause_id}')>"