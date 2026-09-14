import json
import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from app.integrations.voice.deepgram_stt import DeepgramSTTProvider
from app.integrations.voice.elevenlabs_tts import ElevenLabsTTSProvider
from app.services.voice_manager import VoiceManager
from app.core.config import settings # Assuming this exists for API keys

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/incoming")
async def handle_incoming_call(request: Request):
    """
    Webhook called by Twilio when a phone number is dialed.
    Returns TwiML instructing Twilio to open a WebSocket stream.
    """
    # Fix for ngrok: ALWAYS use wss and the host from the header
    host = request.headers.get("host", request.url.hostname)
    ws_url = f"wss://{host}/api/voice/stream"
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Connect>
            <Stream url="{ws_url}" />
        </Connect>
    </Response>
    """
    return HTMLResponse(content=twiml, media_type="text/xml")


@router.websocket("/stream")
async def voice_stream(websocket: WebSocket):
    """
    WebSocket endpoint that receives the bidirectional audio stream from Twilio.
    """
    await websocket.accept()
    
    # Initialize providers
    import os
    from dotenv import load_dotenv
    load_dotenv(r"c:\Users\hp\Desktop\AiReceptionist\.env")
    stt = DeepgramSTTProvider(api_key=os.environ.get("DEEPGRAM_API_KEY", "MOCK_DEEPGRAM_KEY")) # Use settings.DEEPGRAM_API_KEY in prod
    tts = ElevenLabsTTSProvider()
    
    stream_sid = None

    async def send_audio_to_client(audio_chunk: bytes):
        # Twilio requires the streamSid in every media packet!
        if not stream_sid:
            return
            
        payload = {
            "event": "media",
            "streamSid": stream_sid,
            "media": {
                "payload": base64.b64encode(audio_chunk).decode("utf-8")
            }
        }
        await websocket.send_text(json.dumps(payload))
        
    async def send_clear_to_client():
        if not stream_sid:
            return
        payload = {
            "event": "clear",
            "streamSid": stream_sid
        }
        await websocket.send_text(json.dumps(payload))
        
    manager = VoiceManager(
        stt_provider=stt, 
        tts_provider=tts, 
        send_audio_to_client=send_audio_to_client,
        send_clear_to_client=send_clear_to_client
    )
    await manager.start()

    try:
        print("Waiting for Twilio messages...")
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data["event"] == "start":
                stream_sid = data['start']['streamSid']
                print(f"Twilio stream started: {stream_sid}")
            elif data["event"] == "media":
                audio_bytes = base64.b64decode(data["media"]["payload"])
                await manager.ingest_audio(audio_bytes)
            elif data["event"] == "stop":
                print("Twilio stream stopped.")
                break
    except WebSocketDisconnect:
        print("Twilio WebSocket disconnected.")
    finally:
        await manager.stop()
