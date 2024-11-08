# services/auth.py
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None


def login_user(db: Session, login_request: LoginRequest) -> LoginResponse:
    user = authenticate_user(db, login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    expires_at = datetime.now(timezone.utc) + access_token_expires

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_at=expires_at,
    )
