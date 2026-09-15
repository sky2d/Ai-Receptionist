import os
import httpx
import asyncio
import traceback
from typing import AsyncGenerator
from app.integrations.voice.base import TTSProvider

class ElevenLabsTTSProvider(TTSProvider):
    def __init__(self, api_key: str = None, voice_id: str = "pNInz6obpgDQGcFmaJgB"): # Default is 'Adam' voice
        self.api_key = (api_key or os.environ.get("ELEVENLABS_API_KEY", "")).strip()
        self.voice_id = voice_id
        self._text_queue = asyncio.Queue()
        self._audio_queue = asyncio.Queue()
        self._synthesis_task = None
        
    async def connect(self):
        self._synthesis_task = asyncio.create_task(self._synthesize_loop())

    async def _synthesize_loop(self):
        async with httpx.AsyncClient() as client:
            while True:
                text = await self._text_queue.get()
                if text is None:
                    break
                    
                # Request ulaw_8000 format for Twilio compatibility
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream?output_format=ulaw_8000"
                headers = {
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json"
                }
                
                # Must use the multilingual v2 model to support Hindi properly!
                payload = {
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                }
                
                try:
                    async with client.stream("POST", url, headers=headers, json=payload) as response:
                        if response.status_code == 200:
                            async for chunk in response.aiter_bytes():
                                if chunk:
                                    await self._audio_queue.put(chunk)
                        else:
                            print(f"ElevenLabs Error: {response.status_code} - {await response.aread()}")
                except Exception as e:
                    print(f"ElevenLabs Exception: {repr(e)}")
                    traceback.print_exc()

    async def send_text(self, text: str):
        await self._text_queue.put(text)

    async def receive_audio(self) -> AsyncGenerator[bytes, None]:
        while True:
            audio_chunk = await self._audio_queue.get()
            if audio_chunk is None:
                break
            yield audio_chunk

    async def close(self):
        await self._text_queue.put(None)
        await self._audio_queue.put(None)
        if self._synthesis_task:
            self._synthesis_task.cancel()
            
    async def interrupt(self):
        # Cancel the current synthesis task
        if self._synthesis_task:
            self._synthesis_task.cancel()
            
        # Clear the text queue
        while not self._text_queue.empty():
            try:
                self._text_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
                
        # Clear the audio queue
        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
                
        # Restart the synthesis loop
        self._synthesis_task = asyncio.create_task(self._synthesize_loop())
