from .interfaces import AgentInterface
from app.core.config import settings

class AgentManager:
    """
    Responsible for orchestrating the AI Agents.
    Decides which LLM provider to instantiate based on business settings
    or system configuration.
    """
    
    def __init__(self):
        self.default_provider = settings.LLM_PROVIDER
        
    def get_agent(self, business_id: str) -> AgentInterface:
        """
        Factory method to get the correct agent implementation.
        Currently returns a NotImplementedError since we are in the 
        architecture scaffolding phase.
        """
        if self.default_provider == "openai":
            # return OpenAIAgent(...)
            pass
        elif self.default_provider == "anthropic":
            # return AnthropicAgent(...)
            pass
            
        raise NotImplementedError("Agent implementations are scheduled for a future phase.")
