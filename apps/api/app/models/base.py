from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
import uuid

Base = declarative_base()

def generate_uuid() -> str:
    return str(uuid.uuid4())

class TenantModel(Base):
    __abstract__ = True
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    business_id = Column(String, index=True, nullable=False) # Multitenancy key
