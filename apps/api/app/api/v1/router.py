from fastapi import APIRouter
from app.api.routers import knowledge

api_router = APIRouter()

@api_router.get("/status")
def status():
    return {"status": "running"}

api_router.include_router(knowledge.router, prefix="/knowledge")
