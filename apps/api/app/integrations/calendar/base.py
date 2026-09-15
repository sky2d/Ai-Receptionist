from typing import Any, Dict, List, Protocol

class CalendarProvider(Protocol):
    """
    Protocol for any calendar integration (Google, Outlook, Cal.com, etc.)
    """
    
    async def check_availability(self, business_id: str, date: str) -> List[Dict[str, Any]]:
        """Returns available time slots for a given date."""
        ...
        
    async def create_event(self, business_id: str, customer_info: Dict[str, Any], start_time: str, end_time: str) -> Dict[str, Any]:
        """Creates a calendar event and returns event details."""
        ...
        
    async def cancel_event(self, business_id: str, event_id: str) -> bool:
        """Cancels an existing calendar event."""
        ...
