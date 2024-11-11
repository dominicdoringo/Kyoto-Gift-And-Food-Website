# src/app/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.user as user_service
from app.core.auth import get_current_user
from app.dependencies import get_db
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserUpdateResponse,
)
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_all_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: List all users.
    """
    users = user_service.list_users(db=db, current_user=admin_user)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_details_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Get user details by ID.
    """
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserUpdateResponse)
def update_user_info_admin(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Update any user's information.
    """
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = user_service.update_user_admin(db=db, user_id=user_id, user_update=user_update)
    return updated_user


@router.delete("/users/{user_id}", status_code=204)
def delete_user_account_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Delete any user account.
    """
    user_service.delete_user(db=db, user_id=user_id, current_user=admin_user)
    return
