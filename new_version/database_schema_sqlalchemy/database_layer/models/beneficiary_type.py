from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .base import Base

class BeneficiaryType(Base):
    __tablename__ = 'beneficiary_type'
    
    beneficiary_type_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    beneficiary_type_name = Column(String, nullable=False)
    code = Column(Integer, nullable=False, unique=True)
    
    created_at = Column(
        DateTime(timezone=True),
        default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )
    
    def __repr__(self):
        return f"<BeneficiaryType(code={self.code}, name='{self.beneficiary_type_name}')>"