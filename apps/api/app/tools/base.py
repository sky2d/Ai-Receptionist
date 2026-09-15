from typing import Any, Dict, Protocol

class BaseTool(Protocol):
    """
    Protocol for an AI tool that can be executed by the LLM.
    """
    name: str
    description: str

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema definition for the LLM.
        """
        ...
        
    async def execute(self, **kwargs: Any) -> Any:
        """
        Executes the business logic for the tool.
        """
        ...
