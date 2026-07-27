from sqlalchemy.orm import Session as DBSession

from app.models.user import User
from app.models.session import Session as SessionModel
from app.core.security import hash_pin, verify_pin, generate_session_token, session_expiry


def register_user(db: DBSession, name: str, role: str, pin: str) -> User:
    existing = db.query(User).filter(User.name == name).first()
    if existing:
        raise ValueError("A user with this name already exists.")

    user = User(name=name, role=role, pin_hash=hash_pin(pin))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: DBSession, name: str, pin: str) -> SessionModel:
    user = db.query(User).filter(User.name == name).first()
    if not user or not verify_pin(pin, user.pin_hash):
        raise ValueError("Invalid name or PIN.")

    session = SessionModel(
        user_id=user.id,
        token=generate_session_token(),
        expires_at=session_expiry(),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session, user