from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.conversation import Conversation, ConversationStatus, Message, MessageSender
from pydantic import BaseModel

router = APIRouter(prefix="/human", tags=["human_agent"])

class ReplyRequest(BaseModel):
    content: str
    resolve: bool = False

@router.get("/conversations/escalated")
def list_escalated_conversations(business_id: str, db: Session = Depends(get_db)):
    """List all conversations that need human attention."""
    conversations = db.query(Conversation).filter(
        Conversation.business_id == business_id,
        Conversation.status == ConversationStatus.escalated
    ).all()
    return {"conversations": conversations}

@router.get("/conversations/{conversation_id}/messages")
def get_conversation_history(conversation_id: str, db: Session = Depends(get_db)):
    """Get full history of a conversation."""
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).all()
    return {"messages": messages}

@router.post("/conversations/{conversation_id}/reply")
def reply_to_conversation(
    conversation_id: str, 
    request: ReplyRequest, 
    db: Session = Depends(get_db)
):
    """Human replies to a conversation."""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Save the human's message. We label it as 'agent' or perhaps add a new 'human' sender type.
    # For now, 'agent' works, as long as the AI knows it's the assistant side.
    msg = Message(
        conversation_id=conversation_id,
        sender=MessageSender.agent,
        content=f"[Human] {request.content}"
    )
    db.add(msg)
    
    if request.resolve:
        conversation.status = ConversationStatus.active
        
    db.commit()
    
    # NOTE: In a complete implementation, we must push this message down 
    # the corresponding channel (Twilio SMS/Voice WebSocket) using the Channel Adapter.
    # For now, it's just saved in the DB for the frontend to see.
    return {"status": "success"}
