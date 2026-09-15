from typing import List
from pydantic import BaseModel
from .schemas import AgentMessage

class InternalMemory(BaseModel):
    """
    Represents the internal short-term memory / context window for an agent
    during an active conversation session.
    """
    conversation_id: str
    business_id: str
    
    # The system prompt loaded for this business
    system_prompt: str
    
    # The sliding window of recent messages
    messages: List[AgentMessage]
    
    # A summary of older messages that have fallen out of the sliding window
    summary: str = ""
    
    def get_full_context(self) -> List[AgentMessage]:
        """
        Constructs the full message array to send to the LLM.
        System prompt -> Summary (if any) -> Recent messages.
        """
        from .schemas import MessageRole
        
        context = [
            AgentMessage(role=MessageRole.SYSTEM, content=self.system_prompt)
        ]
        
        if self.summary:
            context.append(
                AgentMessage(role=MessageRole.SYSTEM, content=f"Previous conversation summary: {self.summary}")
            )
            
        context.extend(self.messages)
        return context
