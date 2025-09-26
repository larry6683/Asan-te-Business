from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class ShopType(Base):
    __tablename__ = 'shop_type'
    
    shop_type_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    code = Column(
        Integer,
        unique=True,
        nullable=False
    )
    
    shop_type_name = Column(
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
    
    business_shops = relationship("BusinessShop", back_populates="shop_type")
    beneficiary_shops = relationship("BeneficiaryShop", back_populates="shop_type")
    
    def __repr__(self):
        return f"<ShopType(code={self.code}, name='{self.shop_type_name}')>"