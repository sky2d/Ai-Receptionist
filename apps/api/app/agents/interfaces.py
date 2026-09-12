from typing import Protocol, Any
from .schemas import AgentInput, AgentOutput

class AgentInterface(Protocol):
    """
    Protocol defining the contract for all LLM Agents.
    Whether we use OpenAI, Anthropic, or an open-source model,
    it must implement this interface.
    """
    
    async def generate(self, input_data: AgentInput) -> AgentOutput:
        """
        Takes the current context, conversation history, and available tools,
        and generates the next step (either a text response or tool calls).
        """
        ...
