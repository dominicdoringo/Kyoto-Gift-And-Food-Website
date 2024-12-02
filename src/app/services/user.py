# src/app/services/user.py

import secrets
from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.security import verify_password
from app.models.user import User  # SQLAlchemy model
from app.schemas.user import UserCreate, UserUpdate, PasswordChangeRequest
from app.services.email import send_verification_email  # Import the email service
from app.schemas.reward import RewardCreate  # Import the RewardCreate schema
import app.services.reward as reward_service  # Import the reward service

settings = get_settings()

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    # Check if username or email already exists
    if get_user_by_username(db, user.username) or get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Hash the password and generate verification code
    password_hash = bcrypt.hash(user.password)
    verification_code = secrets.token_urlsafe(32)

    # Create a new User instance
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        verification_code=verification_code,
        
    )

    try:
        # Add and commit the new user to the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Automatically enroll the user in the rewards program
        reward_create = RewardCreate(
            user_id=db_user.id,
            reward_tier="Basic",  # Set the default reward tier
            points=0  # Initialize points to 0
        )
        reward_service.create_reward(db=db, user_id=db_user.id, reward=reward_create)

        # Send verification email
        send_verification_email(
            to_email=db_user.email,
            username=db_user.username,
            verification_code=db_user.verification_code
        )

    except SQLAlchemyError as e:
        # Rollback the transaction in case of any database errors
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user.")

    except HTTPException as e:
        # Rollback if sending verification email fails
        db.rollback()
        raise HTTPException(status_code=500, detail="User created but failed to enroll in rewards program or send verification email.")

    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user




def list_users(db: Session, current_user: User):
    """
    Retrieve a list of all users.
    Restricted to admin users only.
    """
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

    if user.id != current_user.id and not current_user.is_admin:
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

    if user.id != current_user.id and not current_user.is_admin:
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

    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to change password for this user")

    if not verify_password(password_change.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.password_hash = bcrypt.hash(password_change.new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully"}


def delete_user_admin(db: Session, user_id: int):
    """
    Admin: Delete any user account without ownership checks.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

def update_user_admin(db: Session, user_id: int, user_update: UserUpdate):
    """
    Admin: Update any user's information without ownership checks.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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