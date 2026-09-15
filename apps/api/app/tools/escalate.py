from typing import Any, Dict
from sqlalchemy.orm import Session
from app.tools.base import BaseTool
from app.models.conversation import Conversation, ConversationStatus

class EscalateTool(BaseTool):
    name = "escalate_to_human"
    description = "Escalates the conversation to a human agent when the user requests it or when the AI cannot answer."

    def __init__(self, db: Session, conversation_id: str):
        self.db = db
        self.conversation_id = conversation_id

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "The reason for escalation"
                        }
                    },
                    "required": ["reason"]
                }
            }
        }
        
    async def execute(self, reason: str, **kwargs: Any) -> Any:
        conversation = self.db.query(Conversation).filter(
            Conversation.id == self.conversation_id
        ).first()
        
        if conversation:
            conversation.status = ConversationStatus.escalated
            self.db.commit()
            return "Escalated successfully. Tell the user a human will be with them shortly."
            
        return "Failed to escalate."
