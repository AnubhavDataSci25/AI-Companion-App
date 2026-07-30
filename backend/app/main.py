from fastapi import FastAPI

from app.api import health, auth, chat, memory, journal, mood, reminder, relationship, admin
from app.core.config import settings

app = FastAPI(title=settings.app_name)

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