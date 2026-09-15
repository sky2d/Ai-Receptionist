from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.models.customer import Customer
from app.models.service import Service

def get_or_create_customer(db: Session, business_id: str, name: str, phone: str) -> Customer:
    # Basic lookup by phone
    customer = db.query(Customer).filter_by(business_id=business_id, phone_number=phone).first()
    if not customer:
        customer = Customer(business_id=business_id, name=name, phone_number=phone)
        db.add(customer)
        db.commit()
        db.refresh(customer)
    return customer

def get_default_service(db: Session, business_id: str) -> Service:
    # For this prototype, we'll just grab any service or create a default one
    service = db.query(Service).filter_by(business_id=business_id).first()
    if not service:
        service = Service(
            business_id=business_id, 
            name="General Consultation", 
            duration_minutes=30,
            price=0.0
        )
        db.add(service)
        db.commit()
        db.refresh(service)
    return service

def check_availability(db: Session, business_id: str, start_time: datetime, end_time: datetime) -> bool:
    """Returns True if the slot is free."""
    overlapping = db.query(Appointment).filter(
        Appointment.business_id == business_id,
        Appointment.status == "scheduled",
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    ).first()
    return overlapping is None

def book_appointment(db: Session, business_id: str, name: str, phone: str, start_time_str: str) -> str:
    """
    Called by the AI Agent Tool.
    start_time_str should be ISO format, e.g. "2024-05-15T14:00:00Z"
    """
    try:
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
    except ValueError:
        return "Failed to book: Invalid time format. Please provide ISO 8601 format."
        
    customer = get_or_create_customer(db, business_id, name, phone)
    service = get_default_service(db, business_id)
    
    end_time = start_time + timedelta(minutes=service.duration_minutes)
    
    if not check_availability(db, business_id, start_time, end_time):
        return "Failed to book: The requested time slot is already booked."
        
    appointment = Appointment(
        business_id=business_id,
        customer_id=customer.id,
        service_id=service.id,
        start_time=start_time,
        end_time=end_time,
        status="scheduled"
    )
    db.add(appointment)
    db.commit()
    
    return f"Successfully booked appointment for {name} at {start_time.strftime('%Y-%m-%d %H:%M')}."

def list_appointments(db: Session, business_id: str) -> list[dict]:
    # Returns a simple dict list for the Dashboard API
    appointments = db.query(Appointment, Customer, Service).join(
        Customer, Appointment.customer_id == Customer.id
    ).join(
        Service, Appointment.service_id == Service.id
    ).filter(
        Appointment.business_id == business_id
    ).order_by(Appointment.start_time).all()
    
    return [
        {
            "id": appt.id,
            "customer_name": cust.name,
            "customer_phone": cust.phone_number,
            "service": svc.name,
            "start_time": appt.start_time.isoformat(),
            "end_time": appt.end_time.isoformat(),
            "status": appt.status
        }
        for appt, cust, svc in appointments
    ]
