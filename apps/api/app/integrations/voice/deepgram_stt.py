import asyncio
from typing import AsyncGenerator
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)
from app.integrations.voice.base import STTProvider

class DeepgramSTTProvider(STTProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        config = DeepgramClientOptions(options={"keepalive": "true"})
        self.deepgram = DeepgramClient(self.api_key, config)
        self.connection = self.deepgram.listen.asynclive.v("1")
        self._text_queue = asyncio.Queue()

    async def connect(self):
        def on_message(self_ws, result, **kwargs):
            try:
                sentence = result.channel.alternatives[0].transcript
                if sentence:
                    print(f"Deepgram heard (final={result.is_final}): {sentence}")
                if sentence and result.is_final:
                    asyncio.create_task(self._text_queue.put(sentence))
            except Exception as e:
                print(f"Deepgram callback error: {e}")
                print(f"Raw result: {result}")

        self.connection.on(LiveTranscriptionEvents.Transcript, on_message)
        
        options = LiveOptions(
            model="nova-2",
            language="hi",
            smart_format=True,
            encoding="mulaw", # Twilio default
            sample_rate=8000, # Twilio default
            channels=1
        )
        await self.connection.start(options)

    async def send_audio(self, audio_data: bytes):
        await self.connection.send(audio_data)

    async def receive_text(self) -> AsyncGenerator[str, None]:
        while True:
            text = await self._text_queue.get()
            if text is None: # Sentinel value for closing
                break
            yield text

    async def close(self):
        await self._text_queue.put(None)
        await self.connection.finish()
