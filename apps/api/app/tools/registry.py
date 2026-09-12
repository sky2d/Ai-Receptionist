from typing import Dict, Any, List
from .base import BaseTool

class ToolRegistry:
    """
    Registry for managing available tools.
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        
    def register(self, tool: BaseTool) -> None:
        """Registers a tool."""
        self._tools[tool.name] = tool
        
    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Returns schemas for all registered tools to send to the LLM."""
        return [tool.get_schema() for tool in self._tools.values()]
        
    async def execute(self, tool_name: str, **kwargs: Any) -> Any:
        """Executes a tool by name."""
        if tool_name not in self._tools:
            raise ValueError(f"Tool {tool_name} not found in registry.")
            
        tool = self._tools[tool_name]
        return await tool.execute(**kwargs)
