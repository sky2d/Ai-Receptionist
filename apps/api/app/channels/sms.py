from typing import Any, Dict
from .base import BaseChannel

class SMSChannel(BaseChannel):
    """
    Handles inbound and outbound SMS communication (e.g., via Twilio).
    """
    
    async def receive_message(self, payload: Dict[str, Any]) -> Any:
        # Skeleton: Normalize Twilio Webhook form data payload
        raise NotImplementedError("SMSChannel scheduled for a future phase.")
        
    async def send_message(self, business_id: str, to: str, content: str) -> bool:
        # Skeleton: Send outbound SMS via Twilio API
        raise NotImplementedError("SMSChannel scheduled for a future phase.")
