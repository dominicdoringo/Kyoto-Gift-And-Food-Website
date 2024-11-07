# schemas/cart.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int


class CartItem(CartItemBase):
    id: int
    name: str
    price: float
    total: float
    created_at: datetime

    class Config:
        from_attributes = True


class CartAddResponse(BaseModel):
    success: bool
    cart: List[CartItem]

    class Config:
        from_attributes = True


class CartUpdateResponse(BaseModel):
    success: bool
    updated_cart: List[CartItem]

    class Config:
        from_attributes = True


class CartRemoveResponse(BaseModel):
    success: bool
    message: str

    class Config:
        from_attributes = True


class CartClearResponse(BaseModel):
    success: bool
    message: str

    class Config:
        from_attributes = True


class CartTotalResponse(BaseModel):
    total: float
    item_count: int

    class Config:
        from_attributes = True


class CartDiscountRequest(BaseModel):
    user_id: int
    discount_code: str


class CartDiscountResponse(BaseModel):
    success: bool
    new_total: float
    discount_applied: str

    class Config:
        from_attributes = True


class CartSaveRequest(BaseModel):
    user_id: int


class CartSaveResponse(BaseModel):
    success: bool
    message: str

    class Config:
        from_attributes = True
