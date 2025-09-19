from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BusinessUser(Base):
    __tablename__ = 'business_user'
    
    business_user_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    business_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business.business_id'),
        nullable=False
    )
    
    app_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('app_user.app_user_id'),
        nullable=False
    )
    
    business_user_permission_role_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business_user_permission_role.business_user_permission_role_id'),
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
    
    business = relationship("Business", back_populates="business_users")
    app_user = relationship("AppUser", back_populates="business_users")
    permission_role = relationship("BusinessUserPermissionRole", back_populates="business_users")
    
    def __repr__(self):
        return f"<BusinessUser(business_id='{self.business_id}', app_user_id='{self.app_user_id}')>"