from fastapi import FastAPI

from app.api import health, auth, chat
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def root():
    return {"message": "Ami is running."}