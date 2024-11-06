# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session
from typing import List

from app import models, crud
from app import schemas
from app.schemas import UserCreate, UserCreateResponse  # Import required schemas directly
from app.dependencies import get_db, get_current_active_user, get_current_active_admin

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return UserCreateResponse(success=True, user=db_user)


@router.get("/", response_model=List[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    return user

@router.put("/{id}", response_model=schemas.UserUpdateResponse)
def update_user(id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, id, user_update)
    return {"success": True, "updatedUser": updated_user}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, id)
    return

@router.put("/{id}/password", response_model=schemas.PasswordChangeResponse)
def change_password(id: int, password_change: schemas.PasswordChangeRequest, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if not crud.verify_password(password_change.oldPassword, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    user.hashed_password = crud.get_password_hash(password_change.newPassword)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": True, "message": "Password updated successfully"}

@router.post("/{id}/profile-picture", response_model=schemas.ProfilePictureResponse)
def upload_profile_picture(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Placeholder for actual file handling logic
    # You would save the file and update the user's profile picture URL
    return {"success": True, "message": "Profile picture uploaded successfully"}

@router.put("/{id}/deactivate", response_model=schemas.DeactivateResponse)
def deactivate_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    # Assuming there is an 'is_active' field in the User model
    user.is_active = False
    db.add(user)
    db.commit()
    return {"success": True, "message": "User account deactivated successfully"}
