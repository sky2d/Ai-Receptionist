from abc import ABC, abstractmethod
from pydantic import BaseModel

class NormalizedMessage(BaseModel):
    channel_id: str
    tenant_id: str
    user_identifier: str
    content: str
    metadata: dict = {}

class ChannelInterface(ABC):
    @abstractmethod
    async def process_incoming(self, raw_payload: dict) -> NormalizedMessage:
        pass

    @abstractmethod
    async def send_outgoing(self, message: str, to: str) -> bool:
        pass
