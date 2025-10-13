from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class RegistrationType(Base):
    __tablename__ = 'registration_type'
    
    registration_type_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    registration_type_name = Column(
        String,
        nullable=False
    )
    
    code = Column(
        Integer,
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
    
    app_users = relationship("AppUserRegistrationType", back_populates="registration_type")
    
    def __repr__(self):
        return f"<RegistrationType(code={self.code}, name='{self.registration_type_name}')>"