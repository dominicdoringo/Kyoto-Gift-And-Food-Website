# app/schemas/order.py

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.product import ProductBase  # Import ProductBase to include imageUrl


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float
    subtotal: float  # Added field
    tax: float       # Added field


class ProductInOrderItem(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderItem(OrderItemBase):
    id: int
    product: ProductInOrderItem  # Include product details with imageUrl

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    payment_method: str


class OrderCreate(OrderBase):
    # Removed cart_items since we fetch them from the database
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None


class Order(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    subtotal: float
    tax: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True


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
