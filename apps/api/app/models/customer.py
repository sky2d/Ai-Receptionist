from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.models.base import TenantModel

class Customer(TenantModel):
    __tablename__ = "customers"
    phone_number = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
