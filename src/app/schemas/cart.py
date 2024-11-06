# schemas/cart.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity of the product")


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="Updated quantity of the product")


class CartItemResponse(CartItemBase):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True


class CartResponse(BaseModel):
    items: List[CartItemResponse]

    class Config:
        orm_mode = True


class CartClearResponse(BaseModel):
    success: bool
    message: str
