from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.models.base import TenantModel, Base, generate_uuid

class KnowledgeDocument(TenantModel):
    __tablename__ = "knowledge_documents"
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    document_id = Column(String, ForeignKey("knowledge_documents.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    # all-MiniLM-L6-v2 has an embedding dimension of 384
    embedding = Column(Vector(384))
