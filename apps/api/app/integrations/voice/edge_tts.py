import asyncio
import edge_tts
from typing import AsyncGenerator
from app.integrations.voice.base import TTSProvider

class EdgeTTSProvider(TTSProvider):
    def __init__(self, voice: str = "en-US-AriaNeural"):
        self.voice = voice
        self._text_queue = asyncio.Queue()
        self._audio_queue = asyncio.Queue()
        self._synthesis_task = None

    async def connect(self):
        self._synthesis_task = asyncio.create_task(self._synthesize_loop())

    async def _synthesize_loop(self):
        while True:
            text = await self._text_queue.get()
            if text is None:
                break
                
            communicate = edge_tts.Communicate(text, self.voice)
            
            # NOTE: Edge TTS outputs MP3 or WebM audio chunks.
            # For Twilio Media Streams, these chunks must be transcoded to 
            # 8000Hz mulaw (G.711) format. A library like `pydub` or a 
            # subprocess calling `ffmpeg` is typically required here before
            # yielding to the audio_queue. 
            # For demonstration, we yield the raw edge-tts chunks.
            
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    await self._audio_queue.put(chunk["data"])
                    
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
