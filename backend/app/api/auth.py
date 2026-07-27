from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", status_code=201)
def register(payload: UserRegister, db: DBSession = Depends(get_db)):
    try:
        user = auth_service.register_user(db, payload.name, payload.role, payload.pin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": str(user.id), "name": user.name, "role": user.role.value}


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: DBSession = Depends(get_db)):
    try:
        session, user = auth_service.login_user(db, payload.name, payload.pin)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return TokenResponse(
        token=session.token,
        role=user.role.value,
        expires_at=session.expires_at.isoformat(),
    )