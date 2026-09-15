from sqlalchemy import Column, String, Integer, Float, Boolean
from app.models.base import TenantModel

class Service(TenantModel):
    __tablename__ = "services"
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
