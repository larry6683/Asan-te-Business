from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base

class BeneficiaryShop(Base):
    __tablename__ = 'beneficiary_shop'
    
    beneficiary_shop_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    beneficiary_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiary.beneficiary_id'),
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
    
    beneficiary = relationship("Beneficiary", back_populates="shops")
    shop_type = relationship("ShopType", back_populates="beneficiary_shops")
    
    def __repr__(self):
        return f"<BeneficiaryShop(beneficiary_id='{self.beneficiary_id}', url='{self.shop_url}')>"