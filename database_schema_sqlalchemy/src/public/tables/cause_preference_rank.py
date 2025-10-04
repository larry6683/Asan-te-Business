from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class CausePreferenceRank(Base):
    __tablename__ = 'cause_preference_rank'
    
    cause_preference_rank_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    cause_preference_rank_name = Column(
        String,
        unique=True,
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
    
    business_preferences = relationship("BusinessCausePreference", back_populates="preference_rank")
    beneficiary_preferences = relationship("BeneficiaryCausePreference", back_populates="preference_rank")  
    
    def __repr__(self):
        return f"<CausePreferenceRank(code={self.code}, name='{self.cause_preference_rank_name}')>"