from typing import List, Dict, Any
from openai import AsyncOpenAI
import os

from .interfaces import AgentInterface
from .schemas import AgentInput, AgentOutput, AgentMessage, MessageRole
from app.core.config import settings # Assuming this has OPENAI_API_KEY

class OpenAIAgent(AgentInterface):
    def __init__(self, model: str = None):
        # We rely on OPENAI_API_KEY in the environment or passed explicitly
        api_key = getattr(settings, "OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
        
        # Automatically detect Groq keys and override base_url
        if api_key and api_key.startswith("gsk_"):
            self.client = AsyncOpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            self.model = model or "openai/gpt-oss-20b"
        else:
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"

    async def generate(self, input_data: AgentInput) -> AgentOutput:
        # Convert internal AgentMessage to OpenAI format
        messages = []
        for msg in input_data.messages:
            openai_msg = {"role": msg.role.value}
            if msg.content is not None:
                openai_msg["content"] = msg.content
            if msg.name is not None:
                openai_msg["name"] = msg.name
            if msg.tool_call_id is not None:
                openai_msg["tool_call_id"] = msg.tool_call_id
            if msg.tool_calls is not None:
                openai_msg["tool_calls"] = msg.tool_calls
            messages.append(openai_msg)

        # Prepare kwargs for the API call
        kwargs = {
            "model": self.model,
            "messages": messages,
        }
        
        if input_data.available_tools:
            kwargs["tools"] = input_data.available_tools
            # We don't force a tool choice by default

        response = await self.client.chat.completions.create(**kwargs)
        
        choice = response.choices[0].message
        
        tool_calls = None
        if choice.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in choice.tool_calls
            ]
            
        usage = None
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }

        return AgentOutput(
            content=choice.content,
            tool_calls=tool_calls,
            usage=usage
        )
