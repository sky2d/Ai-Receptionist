from sqlalchemy.orm import Session
from app.channels.base import NormalizedMessage
from app.models.conversation import Conversation, Message, MessageSender
from app.agents.manager import AgentManager
from app.agents.schemas import AgentInput, AgentMessage, MessageRole

class ConversationEngine:
    def __init__(self, db: Session):
        self.db = db
        self.agent_manager = AgentManager()

    async def handle_message(self, message: NormalizedMessage) -> str:
        # Load conversation
        conversation = self.db.query(Conversation).filter(
            Conversation.id == message.conversation_id,
            Conversation.business_id == message.business_id
        ).first()

        if not conversation:
            # Create new conversation if it doesn't exist
            conversation = Conversation(
                id=message.conversation_id,
                business_id=message.business_id,
                channel=message.channel
            )
            self.db.add(conversation)
            self.db.commit()

        # Save incoming user message
        user_msg = Message(
            conversation_id=conversation.id,
            sender=MessageSender.user,
            content=message.content
        )
        self.db.add(user_msg)
        self.db.commit()

        # Load history
        db_messages = self.db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp.asc()).all()

        agent_messages = []
        # Add system prompt
        agent_messages.append(AgentMessage(
            role=MessageRole.SYSTEM,
            content="You are a helpful AI Receptionist for a business. Answer questions concisely."
        ))

        # Convert DB history to Agent history
        for msg in db_messages:
            role = MessageRole.USER if msg.sender == MessageSender.user else MessageRole.ASSISTANT
            agent_messages.append(AgentMessage(
                role=role,
                content=msg.content
            ))

        if conversation.status == ConversationStatus.escalated:
            # Do not invoke AI. Just save user message and return empty or standard wait message
            return ""

        # Get agent instance
        agent = self.agent_manager.get_agent(business_id=message.business_id)
        
        from app.tools.search_knowledge import SearchKnowledgeTool
        from app.tools.escalate import EscalateTool
        
        search_tool = SearchKnowledgeTool(self.db, message.business_id)
        escalate_tool = EscalateTool(self.db, conversation.id)

        # Invoke agent
        agent_input = AgentInput(
            conversation_id=conversation.id,
            business_id=message.business_id,
            messages=agent_messages,
            available_tools=[search_tool.get_schema(), escalate_tool.get_schema()]
        )
        
        import time
        from app.services.analytics_service import AnalyticsService
        
        start_time = time.time()
        agent_output = await agent.generate(agent_input)
        latency_ms = (time.time() - start_time) * 1000

        response_text = agent_output.content or "I am processing your request."

        # Save assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            sender=MessageSender.agent,
            content=response_text
        )
        self.db.add(assistant_msg)
        self.db.commit()

        # Log analytics
        if agent_output.usage:
            analytics_service = AnalyticsService(self.db)
            analytics_service.log_agent_usage(
                conversation_id=conversation.id,
                business_id=message.business_id,
                usage=agent_output.usage,
                latency_ms=latency_ms
            )

        return response_text
