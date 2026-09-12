from typing import Protocol, Any, Dict

class BaseChannel(Protocol):
    """
    Protocol for any inbound/outbound communication channel (SMS, WebChat, Voice, etc.)
    """
    
    async def receive_message(self, payload: Dict[str, Any]) -> Any:
        """Parses the raw incoming payload into a NormalizedMessage format."""
        ...
        
    async def send_message(self, business_id: str, to: str, content: str) -> bool:
        """Sends an outbound message back through the channel."""
        ...
