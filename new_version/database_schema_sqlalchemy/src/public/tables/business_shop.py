from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BusinessShop(Base):
    __tablename__ = 'business_shop'
    
    business_shop_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    business_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business.business_id'),
        nullable=False
    )
    
    shop_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey('shop_type.shop_type_id'),
        nullable=False
    )
    
    shop_url = Column(
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
    
    business = relationship("Business", back_populates="shops")
    shop_type = relationship("ShopType", back_populates="business_shops")
    
    def __repr__(self):
        return f"<BusinessShop(business_id='{self.business_id}', url='{self.shop_url}')>"