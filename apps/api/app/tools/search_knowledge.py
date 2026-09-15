from typing import Any, Dict
from sqlalchemy.orm import Session
from app.tools.base import BaseTool
from app.services.rag_service import embedding_model
from app.models.knowledge import KnowledgeChunk

class SearchKnowledgeTool(BaseTool):
    name = "search_knowledge"
    description = "Searches the business knowledge base for answers to customer questions."

    def __init__(self, db: Session, business_id: str):
        self.db = db
        self.business_id = business_id

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query based on the user's question"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
        
    async def execute(self, query: str, **kwargs: Any) -> Any:
        query_embedding = embedding_model.encode([query])[0].tolist()
        
        # pgvector L2 distance search (<->)
        results = self.db.query(KnowledgeChunk).order_by(
            KnowledgeChunk.embedding.l2_distance(query_embedding)
        ).limit(3).all()
        
        if not results:
            return "No relevant information found in the knowledge base."
            
        context = "\n\n".join([chunk.content for chunk in results])
        return f"Found the following information:\n{context}"
