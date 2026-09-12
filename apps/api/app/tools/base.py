from abc import ABC, abstractmethod

class ToolInterface(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(self, **kwargs) -> dict:
        pass
