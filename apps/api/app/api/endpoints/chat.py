from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/{business_id}")
async def chat_websocket(websocket: WebSocket, business_id: str):
    """
    WebSocket endpoint for the frontend web chat widget.
    """
    await websocket.accept()
    # Skeleton: Real-time bidirectional loop goes here
    # await websocket.close()
