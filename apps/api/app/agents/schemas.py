from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class AgentMessage(BaseModel):
    role: MessageRole
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

class AgentInput(BaseModel):
    conversation_id: str
    business_id: str
    messages: List[AgentMessage]
    available_tools: List[Dict[str, Any]] = Field(default_factory=list)

class AgentOutput(BaseModel):
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    usage: Optional[Dict[str, int]] = None
