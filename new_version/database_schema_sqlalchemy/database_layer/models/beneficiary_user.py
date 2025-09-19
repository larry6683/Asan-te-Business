from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BeneficiaryUser(Base):
    __tablename__ = 'beneficiary_user'
    
    beneficiary_user_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    beneficiary_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiary.beneficiary_id'),
        nullable=False
    )
    
    app_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('app_user.app_user_id'),
        nullable=False
    )
    
    beneficiary_user_permission_role_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiary_user_permission_role.beneficiary_user_permission_role_id'),
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
    
    beneficiary = relationship("Beneficiary", back_populates="beneficiary_users")
    app_user = relationship("AppUser", back_populates="beneficiary_users")
    permission_role = relationship("BeneficiaryUserPermissionRole", back_populates="beneficiary_users")
    
    def __repr__(self):
        return f"<BeneficiaryUser(beneficiary_id='{self.beneficiary_id}', app_user_id='{self.app_user_id}')>"