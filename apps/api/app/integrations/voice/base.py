from typing import Protocol, AsyncGenerator

class STTProvider(Protocol):
    """
    Protocol for Speech-to-Text streaming providers.
    """
    async def connect(self):
        """Establish connection to the STT provider."""
        ...
        
    async def send_audio(self, audio_data: bytes):
        """Send raw audio chunk to STT provider."""
        ...
        
    async def receive_text(self) -> AsyncGenerator[str, None]:
        """Receive transcripts asynchronously from STT provider."""
        ...
        
    async def close(self):
        """Close connection to STT provider."""
        ...


class TTSProvider(Protocol):
    """
    Protocol for Text-to-Speech streaming providers.
    """
    async def connect(self):
        """Establish connection to the TTS provider."""
        ...
        
    async def send_text(self, text: str):
        """Send text chunk to TTS provider."""
        ...
        
    async def receive_audio(self) -> AsyncGenerator[bytes, None]:
        """Receive synthesized audio asynchronously."""
        ...
        
    async def close(self):
        """Close connection to TTS provider."""
        ...
        
    async def interrupt(self):
        """Interrupt current TTS synthesis and clear queues."""
        ...
