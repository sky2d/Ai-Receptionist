from typing import Any, Dict
from .base import BaseTool
from app.services.appointment_service import AppointmentService

class BookAppointmentTool(BaseTool):
    name = "book_appointment"
    description = "Books an appointment for a customer."
    
    def __init__(self):
        self.service = AppointmentService()
        
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string"},
                        "service_id": {"type": "string"},
                        "start_time": {"type": "string"}
                    },
                    "required": ["customer_id", "service_id", "start_time"]
                }
            }
        }
        
    async def execute(self, **kwargs: Any) -> Any:
        business_id = kwargs.pop("business_id", "placeholder")
        return await self.service.book_appointment(business_id=business_id, **kwargs)
