# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from .. import schemas, crud
from ..dependencies import get_db
from ..security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api", tags=["authentication"])

@router.post("/login", response_model=schemas.AuthTokenResponse)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"success": True, "token": access_token, "user": user}

@router.post("/auth/token/refresh", response_model=schemas.TokenRefreshResponse)
def refresh_token(token_refresh: schemas.TokenRefreshRequest):
    # Placeholder for token refresh logic
    return {"accessToken": "new_access_token"}
