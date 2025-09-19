from sqlalchemy import Column, String, DateTime, ForeignKey, Index, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    
    beneficiary_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    beneficiary_name = Column(
        String,
        unique=True,
        nullable=False
    )
    
    email = Column(
        String,
        unique=True,
        nullable=False
    )
    
    website_url = Column(
        String,
        nullable=True
    )
    
    phone_number = Column(
        String,
        nullable=True
    )
    
    location_city = Column(
        String,
        nullable=False
    )
    
    location_state = Column(
        String,
        nullable=False
    )
    
    ein = Column(
        String,
        nullable=True
    )
    
    beneficiary_description = Column(
        String(512),
        nullable=False,
        default=''
    )
    
    beneficiary_size_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiary_size.beneficiary_size_id'),
        nullable=False
    )
    
    beneficiary_name_hash = Column(
        LargeBinary,
        nullable=True
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
    

    beneficiary_size = relationship("BeneficiarySize", back_populates="beneficiaries")
    beneficiary_users = relationship("BeneficiaryUser", back_populates="beneficiary") 
    cause_preferences = relationship("BeneficiaryCausePreference", back_populates="beneficiary")
    social_media = relationship("BeneficiarySocialMedia", back_populates="beneficiary")
    shops = relationship("BeneficiaryShop", back_populates="beneficiary")
 
    
    def __repr__(self):
        return f"<Beneficiary(name='{self.beneficiary_name}', email='{self.email}')>"
    
Index('beneficiary_beneficiary_name_hash_idx', Beneficiary.beneficiary_name_hash)
Index('beneficiary_email_hash_idx', Beneficiary.email_hash)
