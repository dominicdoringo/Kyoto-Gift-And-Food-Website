# schemas/product.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., example="Deluxe Gift Box")
    description: Optional[str] = Field(None, example="A box filled with assorted gourmet treats.")
    price: float = Field(..., gt=0, example=49.99)
    stock: int = Field(..., ge=0, example=100)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Deluxe Gift Box")
    description: Optional[str] = Field(None, example="A box filled with assorted gourmet treats.")
    price: Optional[float] = Field(None, gt=0, example=49.99)
    stock: Optional[int] = Field(None, ge=0, example=100)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
