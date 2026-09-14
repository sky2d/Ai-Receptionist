import asyncio
import json
import logging
from typing import Callable, Awaitable
from datetime import datetime
from openai import AsyncOpenAI
import os
from app.integrations.voice.base import STTProvider, TTSProvider
from app.db.session import SessionLocal
from app.services.calendar_service import book_appointment
from app.services.document_processor import search_knowledge_base

logger = logging.getLogger(__name__)

# System prompt sets the persona and instructions
SYSTEM_PROMPT = """You are a highly capable AI Receptionist for our business.
You are talking to a customer over the phone. Your responses must be concise, conversational, and helpful.
Use the provided tools to lookup information from our knowledge base to answer questions, or to book appointments.
If you don't know the answer, politely tell them. Do not hallucinate.
When booking appointments, ask for their name, phone number, and desired time. 
Confirm the time with them before booking, and assume the year is the current year.
Current Time Context: {current_time}
"""

class VoiceManager:
    """
    Coordinates the low-latency streaming audio pipeline:
    Client Audio -> STT -> LLM Agent (with Tools) -> TTS -> Client Audio
    """
    def __init__(
        self, 
        stt_provider: STTProvider, 
        tts_provider: TTSProvider,
        send_audio_to_client: Callable[[bytes], Awaitable[None]],
        send_clear_to_client: Callable[[], Awaitable[None]] = None
    ):
        self.stt = stt_provider
        self.tts = tts_provider
        self.send_audio_to_client = send_audio_to_client
        self.send_clear_to_client = send_clear_to_client
        self._running = False
        
        # Configure OpenAI client to point to Groq since user provided a Groq key
        self.llm_client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"), # the gsk_ key
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "openai/gpt-oss-20b" # User specified model
        
        # Default business ID for prototype
        self.business_id = "00000000-0000-0000-0000-000000000000"
        
        self.chat_history = [
            {"role": "system", "content": SYSTEM_PROMPT.format(current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        ]
        self._current_llm_task = None
        
    async def start(self):
        self._running = True
        await self.stt.connect()
        await self.tts.connect()
        
        # Greet the user when they connect
        initial_greeting = "Hello! Thanks for calling. How can I help you today?"
        self.chat_history.append({"role": "assistant", "content": initial_greeting})
        await self.tts.send_text(initial_greeting)
        
        self._stt_task = asyncio.create_task(self._stt_to_agent_loop())
        self._tts_task = asyncio.create_task(self._tts_to_client_loop())

    async def ingest_audio(self, audio_chunk: bytes):
        if self._running:
            await self.stt.send_audio(audio_chunk)

    async def _stt_to_agent_loop(self):
        try:
            async for user_text in self.stt.receive_text():
                print(f"User said: {user_text}")
                
                # BARGE-IN: If the user speaks, interrupt any ongoing AI processing or talking
                if self._current_llm_task and not self._current_llm_task.done():
                    print("Interrupting AI thought process...")
                    self._current_llm_task.cancel()
                    
                await self.tts.interrupt()
                
                if self.send_clear_to_client:
                    await self.send_clear_to_client()
                    
                self.chat_history.append({"role": "user", "content": user_text})
                
                # Execute LLM step
                self._current_llm_task = asyncio.create_task(self._process_llm_turn())
                
        except Exception as e:
            print(f"Error in STT loop: {e}")

    async def _process_llm_turn(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": "Searches the business documents to answer customer questions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query."}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "book_appointment",
                    "description": "Books an appointment on the calendar.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "phone": {"type": "string"},
                            "start_time_iso": {"type": "string", "description": "ISO 8601 string, e.g. 2024-05-15T14:00:00Z"}
                        },
                        "required": ["name", "phone", "start_time_iso"]
                    }
                }
            }
        ]
        
        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=self.chat_history,
                tools=tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            self.chat_history.append(message)
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    fn_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    print(f"Agent invoking tool: {fn_name} with {args}")
                    
                    db = SessionLocal()
                    try:
                        if fn_name == "search_knowledge_base":
                            results = search_knowledge_base(db, args["query"], self.business_id)
                            tool_response = "\n".join(results) if results else "No information found."
                        elif fn_name == "book_appointment":
                            tool_response = book_appointment(db, self.business_id, args["name"], args["phone"], args["start_time_iso"])
                        else:
                            tool_response = "Unknown function."
                    finally:
                        db.close()
                        
                    self.chat_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": fn_name,
                        "content": tool_response
                    })
                
                # Make a follow up call with the tool results
                second_response = await self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=self.chat_history
                )
                final_text = second_response.choices[0].message.content
                self.chat_history.append(second_response.choices[0].message)
            else:
                final_text = message.content
                
            print(f"Agent replied: {final_text}")
            await self.tts.send_text(final_text)
            
        except asyncio.CancelledError:
            print("LLM Task was cancelled due to user barge-in.")
        except Exception as e:
            print(f"LLM Error: {e}")
            await self.tts.send_text("I'm sorry, I'm having trouble processing that right now.")

    async def _tts_to_client_loop(self):
        try:
            async for audio_chunk in self.tts.receive_audio():
                await self.send_audio_to_client(audio_chunk)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error in TTS loop: {e}")

    async def stop(self):
        self._running = False
        await self.stt.close()
        await self.tts.close()
        if hasattr(self, "_stt_task"):
            self._stt_task.cancel()
        if hasattr(self, "_tts_task"):
            self._tts_task.cancel()
