from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api import health, auth, chat, memory, journal, mood, reminder, relationship, admin
from app.core.config import settings
from app.core.logging_config import setup_logging, logger
from app.core.rate_limit import limiter
 
setup_logging()

app = FastAPI(title=settings.app_name)

# Rate limiting — protects against abuse/brute-force, especially on /auth
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
 
# CORS — permissive for local dev; tighten to your app's domain before production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to Flutter app's origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on Ami's side. Please try again."},
    )

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(memory.router, prefix="/api/memories", tags=["memories"])
app.include_router(journal.router, prefix="/api/journal", tags=["journal"])
app.include_router(mood.router, prefix="/api/mood", tags=["mood"])
app.include_router(reminder.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(relationship.router, prefix="/api/relationship", tags=["relationship"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Ami is running."}
