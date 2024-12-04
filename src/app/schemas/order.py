# app/schemas/order.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductBase

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float
    subtotal: float
    tax: float

class ProductInOrderItem(ProductBase):
    id: int

    class Config:
        orm_mode = True

class OrderItem(OrderItemBase):
    id: int
    product: ProductInOrderItem

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    payment_method: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None

class Order(OrderBase):
    id: int
    user_id: int
    status: str
    total: float
    subtotal: float
    tax: float
    created_at: datetime
    updated_at: datetime
    user: UserBase  # Include user information
    items: List[OrderItem]

    class Config:
        orm_mode = True

# ... other schemas remain unchanged


class OrderCreateResponse(BaseModel):
    success: bool
    order_id: int
    total: float
    status: str
    reward_points: int

    class Config:
        orm_mode = True


class OrderUpdateResponse(BaseModel):
    success: bool
    updated_order: Order

    class Config:
        orm_mode = True


class OrderStatusHistory(BaseModel):
    status: str
    date: datetime

    class Config:
        orm_mode = True
