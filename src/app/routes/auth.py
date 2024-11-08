# routes/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import login_user

router = APIRouter()


@router.post("/login", response_model=LoginResponse, tags=["Authentication"])
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, login_request)
