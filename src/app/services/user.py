# src/app/services/user.py

import secrets
from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import verify_password
from app.models.user import User  # SQLAlchemy model
from app.schemas.user import UserCreate
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
