import os
import httpx
import asyncio
from typing import AsyncGenerator
from app.integrations.voice.base import TTSProvider

class DeepgramTTSProvider(TTSProvider):
    def __init__(self, api_key: str = None, voice: str = "aura-asteria-en"):
        self.api_key = api_key or os.environ.get("DEEPGRAM_API_KEY")
        self.voice = voice
        self._text_queue = asyncio.Queue()
        self._audio_queue = asyncio.Queue()
        self._synthesis_task = None
        
    async def connect(self):
        self._synthesis_task = asyncio.create_task(self._synthesize_loop())

    async def _synthesize_loop(self):
        # We use httpx to stream the audio chunks directly from Deepgram
        async with httpx.AsyncClient() as client:
            while True:
                text = await self._text_queue.get()
                if text is None:
                    break
                    
                # Request mulaw 8000Hz format for Twilio compatibility
                url = f"https://api.deepgram.com/v1/speak?model={self.voice}&encoding=mulaw&sample_rate=8000"
                headers = {
                    "Authorization": f"Token {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {"text": text}
                
                try:
                    async with client.stream("POST", url, headers=headers, json=payload) as response:
                        if response.status_code == 200:
                            async for chunk in response.aiter_bytes():
                                if chunk:
                                    await self._audio_queue.put(chunk)
                        else:
                            print(f"Deepgram TTS Error: {response.status_code} - {await response.aread()}")
                except Exception as e:
                    print(f"Deepgram TTS Exception: {e}")

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
