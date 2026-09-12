from abc import ABC, abstractmethod
from typing import List

class AgentInterface(ABC):
    @abstractmethod
    async def generate_response(self, context: List[dict], user_intent: str) -> str:
        pass
