import uuid

from sqlalchemy.orm import Session as DBSession

from app.models.admin_log import AdminLog


def log_admin_action(db: DBSession, admin_id: uuid.UUID, action: str, detail: str = ""):
    db.add(AdminLog(admin_id=admin_id, action=action, detail=detail))
    db.commit()