from datetime import datetime

from app.workers.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.reminder import Reminder


@celery_app.task
def check_due_reminders():
    db = SessionLocal()
    try:
        due = (
            db.query(Reminder)
            .filter(Reminder.sent == False, Reminder.remind_at <= datetime.utcnow())  # noqa: E712
            .all()
        )
        for reminder in due:
            # NOTE: actual push notification via Firebase Cloud Messaging is wired in a later phase.
            # For now we just mark it sent so it's picked up by the app on next sync.
            print(f"[reminder] Due: {reminder.title} (user {reminder.user_id})")
            reminder.sent = True
        db.commit()
        return f"Checked reminders, {len(due)} due."
    finally:
        db.close()