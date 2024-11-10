# src/app/schemas/user.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):  # Renamed from 'User' to 'UserSchema'
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Use 'orm_mode' instead of 'from_attributes'


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# **New Schemas**

class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None  # Allows activation/deactivation


class UserUpdateResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


class PasswordChangeResponse(BaseModel):
    message: str


class DeactivateResponse(BaseModel):
    message: str
