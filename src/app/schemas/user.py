# src/app/schemas/user.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserDetailResponse(UserResponse):
    cart_items: Optional[list] = None
    orders: Optional[list] = None
    reward: Optional[dict] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True
