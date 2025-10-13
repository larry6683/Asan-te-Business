from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BeneficiaryUserPermissionRole(Base):
    __tablename__ = 'beneficiary_user_permission_role'
    
    beneficiary_user_permission_role_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    beneficiary_user_permission_role_name = Column(
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
    
  
    beneficiary_users = relationship("BeneficiaryUser", back_populates="permission_role")
    
    def __repr__(self):
        return f"<BeneficiaryUserPermissionRole(code={self.code}, name='{self.beneficiary_user_permission_role_name}')>"