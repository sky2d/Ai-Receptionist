from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import Base, TenantModel, generate_uuid

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Business(Base):
    __tablename__ = "businesses"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    timezone = Column(String, default="UTC")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
