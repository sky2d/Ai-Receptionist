from fastapi import APIRouter
from .chat import router as chat_router
from .sms import router as sms_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(sms_router, prefix="/sms", tags=["sms"])
