from typing import Any, Dict
from .base import BaseChannel

class WebChatChannel(BaseChannel):
    """
    Handles bidirectional WebChat communication (typically via WebSockets).
    """
    
    async def receive_message(self, payload: Dict[str, Any]) -> Any:
        # Skeleton: Normalize WebSocket JSON payload
        raise NotImplementedError("WebChatChannel scheduled for a future phase.")
        
    async def send_message(self, business_id: str, to: str, content: str) -> bool:
        # Skeleton: Broadcast message back to the active WebSocket connection
        raise NotImplementedError("WebChatChannel scheduled for a future phase.")
