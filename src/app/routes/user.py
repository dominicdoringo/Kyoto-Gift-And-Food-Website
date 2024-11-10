# src/app/routes/user.py

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.services.user as user_service
from app.core.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from app.dependencies import get_db 
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse, UserSchema  # Updated import
from app.models.user import User  # Import SQLAlchemy User model

router = APIRouter()

@router.post("/register", response_model=UserResponse, tags=["Users"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)

@router.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = user_service.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": datetime.now(timezone.utc) + access_token_expires,
    }

@router.get("/users", response_model=UserResponse, tags=["Users"])
def read_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retrieve the currently authenticated user's details.
    """
    return current_user

@router.get("/verify-email/{verification_code}", tags=["Users"])
def verify_email(verification_code: str, db: Session = Depends(get_db)):
    """
    Verify a user's email address using the provided verification code.
    """
    user = db.query(User).filter(User.verification_code == verification_code).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code."
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified."
        )
    
    user.is_verified = True
    user.verification_code = None  # Optionally, remove the verification code after verification
    db.commit()
    db.refresh(user)
    #ISSUE : DOES NOT WORK WITH MOBILE EMAIL CLICK LINK DOESNT WORK??? But works with desktop email. 
    return {"message": "Email successfully verified."}
