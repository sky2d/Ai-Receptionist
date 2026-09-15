from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.v1.router import api_router
from app.api.routers import voice_webhook, human_agent
from app.core.logging import setup_logging
import time

logger = setup_logging()
limiter = Limiter(key_func=get_remote_address)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Receptionist API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info("API Request", extra={
            "path": request.url.path,
            "method": request.method,
            "process_time": process_time,
            "status_code": response.status_code
        })
        return response

app.add_middleware(TelemetryMiddleware)

app.include_router(api_router, prefix="/api/v1")
app.include_router(voice_webhook.router, prefix="/api")
app.include_router(human_agent.router, prefix="/api")

@app.get("/health")
@limiter.limit("10/minute")
def health_check(request: Request):
    return {"status": "ok"}

