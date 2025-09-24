from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BusinessSize(Base):
    __tablename__ = 'business_size'
    
    business_size_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    business_size_name = Column(
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
    
    businesses = relationship("Business", back_populates="business_size")
    
    def __repr__(self):
        return f"<BusinessSize(code={self.code}, name='{self.business_size_name}')>"