import secrets
from datetime import datetime, timedelta

import bcrypt

SESSION_EXPIRY_HOURS = 12
BCRYPT_MAX_BYTES = 72


def _validate_bcrypt_input(value: str) -> None:
    if len(value.encode("utf-8")) > BCRYPT_MAX_BYTES:
        raise ValueError("PIN is too long.")


def hash_pin(pin: str) -> str:
    _validate_bcrypt_input(pin)
    return bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_pin(pin: str, pin_hash: str) -> bool:
    _validate_bcrypt_input(pin)
    return bcrypt.checkpw(pin.encode("utf-8"), pin_hash.encode("utf-8"))


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def session_expiry() -> datetime:
    return datetime.utcnow() + timedelta(hours=SESSION_EXPIRY_HOURS)
