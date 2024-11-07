# schemas/order_item.py

from pydantic import BaseModel, Field
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity of the product")
    price: float = Field(..., gt=0, description="Price of the product at the time of ordering")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, description="Updated quantity of the product")
    price: Optional[float] = Field(None, gt=0, description="Updated price of the product at the time of ordering")

class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        orm_mode = True
