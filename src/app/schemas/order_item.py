# schemas/order_item.py

from pydantic import BaseModel, Field
from typing import Optional

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity of the product")
    price: float = Field(..., gt=0, description="Price of the product at the time of ordering")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True
