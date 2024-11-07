# schema product.py
from datetime import datetime
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str
    stock: int
    featured: bool = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    stock: int | None = None
    featured: bool | None = None


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    category: str
    stock: int
    featured: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    success: bool
    product: Product

    class Config:
        from_attributes = True
