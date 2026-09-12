from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class TenantModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(String, index=True) # Multitenancy key
