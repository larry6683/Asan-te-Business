from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .base import Base

class BeneficiarySocialMedia(Base):
    __tablename__ = 'beneficiary_social_media'
    
    beneficiary_social_media_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    beneficiary_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiary.beneficiary_id'),
        nullable=False
    )
    social_media_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey('social_media_type.social_media_type_id'),
        nullable=False
    )
    social_media_url = Column(
        String,
        nullable=False,
        unique=True
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
    
    beneficiary = relationship("Beneficiary", back_populates="social_media")
    social_media_type = relationship("SocialMediaType", back_populates="beneficiary_social_media")
    
    def __repr__(self):
        return f"<BeneficiarySocialMedia(beneficiary_id='{self.beneficiary_id}', url='{self.social_media_url}')>"