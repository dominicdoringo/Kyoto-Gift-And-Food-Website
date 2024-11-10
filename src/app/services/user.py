# src/app/services/user.py

import secrets
from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import verify_password
from app.models.user import User  # SQLAlchemy model
from app.schemas.user import UserCreate, UserUpdate, PasswordChangeRequest
from app.services.email import send_verification_email  # Import the email service

settings = get_settings()

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Register a new user
def create_user(db: Session, user: UserCreate):
    if get_user_by_username(db, user.username) or get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")

    password_hash = bcrypt.hash(user.password)
    verification_code = secrets.token_urlsafe(32)

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        verification_code=verification_code,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send verification email
    try:
        send_verification_email(
            to_email=db_user.email,
            username=db_user.username,
            verification_code=db_user.verification_code
        )
    except HTTPException as e:
        # Optionally, handle email sending failure (e.g., rollback user creation)
        raise HTTPException(status_code=500, detail="User created but failed to send verification email.")

    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


# **New Service Functions**

def list_users(db: Session, current_user: User):
    """
    Retrieve a list of all users.
    For security, you might want to restrict this to admin users.
    Currently, it allows any authenticated user to view all users.
    """
    # OPTIONAL: Restrict to admin users
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view all users")
    users = db.query(User).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_update: UserUpdate, current_user: User):
    """
    Update user information.
    Users can only update their own information.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    if user_update.username:
        if user_update.username != user.username and get_user_by_username(db, user_update.username):
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = user_update.username

    if user_update.email:
        if user_update.email != user.email and get_user_by_email(db, user_update.email):
            raise HTTPException(status_code=400, detail="Email already taken")
        user.email = user_update.email

    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int, current_user: User):
    """
    Delete a user account.
    Users can only delete their own account.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    db.delete(user)
    db.commit()
    return


def change_password(db: Session, user_id: int, password_change: PasswordChangeRequest, current_user: User):
    """
    Change a user's password.
    Users can only change their own password.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to change password for this user")

    if not verify_password(password_change.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.password_hash = bcrypt.hash(password_change.new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully"}


def deactivate_user(db: Session, user_id: int, current_user: User):
    """
    Deactivate a user's account.
    Users can only deactivate their own account.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to deactivate this user")

    user.is_active = False
    db.commit()
    db.refresh(user)
    return {"message": "User account deactivated successfully"}
