# database_layer/models/business.py
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, LargeBinary, event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import hashlib 

from .base import Base

class Business(Base):
    __tablename__ = 'business'
    
    business_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    business_name = Column(
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
    
    business_description = Column(
        String(512),
        nullable=False,
        default=''
    )
    
    business_size_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business_size.business_size_id'),
        nullable=False
    )
    
    business_name_hash = Column(
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
    
    business_size = relationship("BusinessSize", back_populates="businesses")
    business_users = relationship("BusinessUser", back_populates="business")
    cause_preferences = relationship("BusinessCausePreference", back_populates="business")
    social_media = relationship("BusinessSocialMedia", back_populates="business")
    shops = relationship("BusinessShop", back_populates="business")
    impact_links = relationship("BusinessImpactLink", back_populates="business")  
    
    def __repr__(self):
        return f"<Business(name='{self.business_name}', email='{self.email}')>"

Index('business_business_name_hash_idx', Business.business_name_hash)
Index('business_email_hash_idx', Business.email_hash)

@event.listens_for(Business, 'before_insert')
@event.listens_for(Business, 'before_update')
def populate_business_hashes(mapper, connection, target):
    """Auto-populate hash fields on insert/update - replaces original PostgreSQL triggers"""
    if target.business_name:
        target.business_name_hash = hashlib.md5(target.business_name.lower().encode()).digest()
    if target.email:
        target.email_hash = hashlib.md5(target.email.lower().encode()).digest()