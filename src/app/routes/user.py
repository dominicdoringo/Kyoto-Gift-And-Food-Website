# routes/user.py

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.services.user as user_service
from app.core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    oauth2_scheme,
)
from app.dependencies import get_db
from app.schemas.token import Token, AuthTokenResponse
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserUpdateResponse,
    UserDeleteResponse,
    UserDeactivateResponse,
    PasswordChangeRequest,
    PasswordChangeResponse,
    ProfilePictureResponse,
    DeactivateResponse,
    UserLogin,
)
from app.models.user import User

router = APIRouter()

#Register a New User (POST /api/users)
@router.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user_service.create_user(db=db, user=user)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return new_user

#List all Users (GET /api/users) ADMIN ONLY
@router.get("/api/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_service.get_all_users(db=db)

#Get user Details by ID (GET /api/users/{id})
@router.get("/api/users/{id}", response_model=UserResponse)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = user_service.get_user_by_id(db=db, user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return user

#Update User Information (PUT /api/users/{id})
@router.put("/api/users/{id}", response_model=UserUpdateResponse)
def update_user(
    id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    updated_user = user_service.update_user(db=db, user_id=id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "updatedUser": updated_user}

#Delete User (DELETE /api/users/{id})
@router.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    success = user_service.delete_user(db=db, user_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Change User Password (POST /api/users/change-password)
@router.put("/api/users/{id}/password", response_model=PasswordChangeResponse)
def change_password(
    id: int,
    password_change: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to change this user's password")
    success = user_service.change_user_password(
        db=db,
        user_id=id,
        old_password=password_change.oldPassword,
        new_password=password_change.newPassword,
    )
    if not success:
        raise HTTPException(status_code=400, detail="Invalid old password")
    return {"success": True, "message": "Password updated successfully"}

#Upload Profile Picture (POST /api/users/{id}/profile-picture)
@router.post("/api/users/{id}/profile-picture", response_model=ProfilePictureResponse)
def upload_profile_picture(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to upload profile picture for this user")
    result = user_service.save_profile_picture(user_id=id, file=file)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid file")
    return {"success": True, "message": "Profile picture uploaded successfully"}

#Deactivate User Account (POST /api/users/{id}/deactivate)
@router.put("/api/users/{id}/deactivate", response_model=DeactivateResponse)
def deactivate_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to deactivate this user")
    success = user_service.deactivate_user(db=db, user_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": "User account deactivated successfully"}

#Authenticate User amd Generate Access Token (POST /api/users/login)
@router.post("/api/login", response_model=AuthTokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_service.authenticate_user(
        db=db,
        email=form_data.username,  # OAuth2PasswordRequestForm uses 'username' field
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"success": True, "token": access_token, "user": user}

#Get Current User Details (GET /api/users/me)
@router.get("/api/users/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

#verify User Email (POST /api/users/verify-email)
@router.post("/api/users/verify-email/{verification_code}")
def verify_email(
    verification_code: str,
    db: Session = Depends(get_db),
):
    success = user_service.verify_user_email(db=db, code=verification_code)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return {"success": True, "message": "Email verified successfully"}
