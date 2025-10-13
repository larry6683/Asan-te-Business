from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .base import Base

class SocialMediaType(Base):
    __tablename__ = 'social_media_type'
    
    social_media_type_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    social_media_type_name = Column(
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

    business_social_media = relationship("BusinessSocialMedia", back_populates="social_media_type")
    beneficiary_social_media = relationship("BeneficiarySocialMedia", back_populates="social_media_type")
    
    def __repr__(self):
        return f"<SocialMediaType(code={self.code}, name='{self.social_media_type_name}')>"