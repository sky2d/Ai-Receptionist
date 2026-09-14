from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import TenantModel

class ConversationAnalytics(TenantModel):
    __tablename__ = "conversation_analytics"

    conversation_id = Column(String, ForeignKey("conversations.id"), index=True)
    
    total_tokens_used = Column(Float, default=0.0)
    prompt_tokens = Column(Float, default=0.0)
    completion_tokens = Column(Float, default=0.0)
    
    # Latency in milliseconds
    average_latency_ms = Column(Float, default=0.0)
    
    # Store any tool execution errors or specific event logs
    events = Column(JSON, default=list)
    
    conversation = relationship("Conversation", backref="analytics")
