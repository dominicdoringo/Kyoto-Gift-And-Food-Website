# schemas/order.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.schemas.order_item import OrderItemCreate, OrderItemResponse

class OrderBase(BaseModel):
    user_id: int
    total_price: float = Field(..., gt=0, description="Total price of the order")
    status: str = Field(..., description="Status of the order")
    address: str = Field(..., description="Shipping address for the order")

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    address: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
