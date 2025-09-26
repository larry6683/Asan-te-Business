from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Index, LargeBinary, event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import hashlib

from .base import Base

class AppUser(Base):
    __tablename__ = 'app_user'
    
    app_user_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    user_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user_type.user_type_id'),
        nullable=False
    )
    
    email = Column(
        String,
        nullable=False
    )
    
    mailing_list_signup = Column(
        Boolean,
        nullable=False,
        default=False
    )
    
    email_hash = Column(
        LargeBinary,
        nullable=True
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
    
    user_type = relationship("UserType", back_populates="app_users")
    registration_types = relationship("AppUserRegistrationType", back_populates="app_user")
    business_users = relationship("BusinessUser", back_populates="app_user")
    beneficiary_users = relationship("BeneficiaryUser", back_populates="app_user")  # Add this line
    
    def __repr__(self):
        return f"<AppUser(email='{self.email}', user_type_id='{self.user_type_id}')>"

Index('app_user_email_hash_idx', AppUser.email_hash)

@event.listens_for(AppUser, 'before_insert')
@event.listens_for(AppUser, 'before_update')
def populate_app_user_hashes(mapper, connection, target):
    if target.email:
        target.email_hash = hashlib.md5(target.email.lower().encode()).digest()