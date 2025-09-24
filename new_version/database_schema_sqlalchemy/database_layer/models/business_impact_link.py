from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BusinessImpactLink(Base):
    __tablename__ = 'business_impact_link'
    
    business_impact_link_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    business_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business.business_id'),
        nullable=False
    )
    
    impact_link_url = Column(
        String,
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
    
    business = relationship("Business", back_populates="impact_links")
    
    def __repr__(self):
        return f"<BusinessImpactLink(business_id='{self.business_id}', url='{self.impact_link_url}')>"