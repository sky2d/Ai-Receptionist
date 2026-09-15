from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.models.base import TenantModel, Base, generate_uuid

class ChannelType(str, enum.Enum):
    web = "web"
    sms = "sms"
    phone = "phone"
    whatsapp = "whatsapp"

class ConversationStatus(str, enum.Enum):
    active = "active"
    closed = "closed"
    escalated = "escalated"

class MessageSender(str, enum.Enum):
    user = "user"
    agent = "agent"
    system = "system"

class Conversation(TenantModel):
    __tablename__ = "conversations"
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    channel = Column(Enum(ChannelType), nullable=False)
    status = Column(Enum(ConversationStatus), default=ConversationStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    sender = Column(Enum(MessageSender), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
