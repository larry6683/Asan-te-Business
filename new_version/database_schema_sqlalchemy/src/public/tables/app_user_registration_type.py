from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class AppUserRegistrationType(Base):
    __tablename__ = 'app_user_registration_type'
    
    app_user_registration_type_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    app_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('app_user.app_user_id'),
        nullable=False
    )
    
    registration_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey('registration_type.registration_type_id'),
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
    
    app_user = relationship("AppUser", back_populates="registration_types")
    registration_type = relationship("RegistrationType", back_populates="app_users")
    
    def __repr__(self):
        return f"<AppUserRegistrationType(app_user_id='{self.app_user_id}', registration_type_id='{self.registration_type_id}')>"