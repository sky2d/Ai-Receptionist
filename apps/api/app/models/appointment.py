from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
import enum
from app.models.base import TenantModel

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"

class Appointment(TenantModel):
    __tablename__ = "appointments"
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    service_id = Column(String, ForeignKey("services.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
