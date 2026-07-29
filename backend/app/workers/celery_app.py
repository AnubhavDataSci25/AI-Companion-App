from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "ami",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.reminder_tasks"],
)

celery_app.conf.beat_schedule = {
    "check-due-reminders-every-minute": {
        "task": "app.workers.reminder_tasks.check_due_reminders",
        "schedule": crontab(minute="*"),
    },
}
celery_app.conf.timezone = "UTC"