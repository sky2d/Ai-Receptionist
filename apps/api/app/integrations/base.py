from abc import ABC, abstractmethod

class CalendarProvider(ABC):
    @abstractmethod
    async def check_availability(self, start_time: str, end_time: str) -> bool:
        pass

    @abstractmethod
    async def create_appointment(self, details: dict) -> str:
        pass
