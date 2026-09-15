from sqlalchemy.orm import Session
from app.models.analytics import ConversationAnalytics

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def log_agent_usage(self, conversation_id: str, business_id: str, usage: dict, latency_ms: float):
        if not usage:
            return
            
        analytics = self.db.query(ConversationAnalytics).filter(
            ConversationAnalytics.conversation_id == conversation_id
        ).first()
        
        if not analytics:
            analytics = ConversationAnalytics(
                conversation_id=conversation_id,
                business_id=business_id,
                total_tokens_used=0,
                prompt_tokens=0,
                completion_tokens=0,
                average_latency_ms=0,
                events=[]
            )
            self.db.add(analytics)
            self.db.flush()
            
        # Update tokens
        analytics.total_tokens_used += usage.get("total_tokens", 0)
        analytics.prompt_tokens += usage.get("prompt_tokens", 0)
        analytics.completion_tokens += usage.get("completion_tokens", 0)
        
        if analytics.average_latency_ms == 0:
            analytics.average_latency_ms = latency_ms
        else:
            analytics.average_latency_ms = (analytics.average_latency_ms + latency_ms) / 2.0
            
        self.db.commit()
