from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BusinessUserPermissionRole(Base):
    __tablename__ = 'business_user_permission_role'
    
    business_user_permission_role_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    business_user_permission_role_name = Column(
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
    
    business_users = relationship("BusinessUser", back_populates="permission_role")
    
    def __repr__(self):
        return f"<BusinessUserPermissionRole(code={self.code}, name='{self.business_user_permission_role_name}')>"