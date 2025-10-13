from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class Cause(Base):
    __tablename__ = 'cause'
    
    cause_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    cause_name = Column(
        String,
        unique=True,
        nullable=False
    )
    
    cause_category_id = Column(
        UUID(as_uuid=True),
        ForeignKey('cause_category.cause_category_id'),
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
    
    cause_category = relationship("CauseCategory", back_populates="causes")
    business_preferences = relationship("BusinessCausePreference", back_populates="cause")
    beneficiary_preferences = relationship("BeneficiaryCausePreference", back_populates="cause") 
    
    def __repr__(self):
        return f"<Cause(code={self.code}, name='{self.cause_name}')>"