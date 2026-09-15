from app.models.base import Base, TenantModel
from app.models.user import User, Business
from app.models.customer import Customer
from app.models.service import Service
from app.models.appointment import Appointment
from app.models.conversation import Conversation, Message
from app.models.analytics import ConversationAnalytics
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk

# Expose all models so Alembic can import them easily
__all__ = [
    "Base",
    "TenantModel",
    "User",
    "Business",
    "Customer",
    "Service",
    "Appointment",
    "Conversation",
    "Message",
    "ConversationAnalytics",
    "KnowledgeDocument",
    "KnowledgeChunk"
]
