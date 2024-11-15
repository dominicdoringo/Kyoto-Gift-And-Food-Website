# schemas/cart.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.product import ProductBase


class CartItemBase(BaseModel):
    quantity: int = 1


class CartItemCreate(CartItemBase):
    product_id: int
    user_id: int


class CartItemUpdate(BaseModel):
    quantity: int


class ProductInCart(ProductBase):
    id: int

    class Config:
        orm_mode = True


class CartItem(CartItemBase):
    id: int
    user_id: int
    product: ProductInCart
    created_at: datetime

    class Config:
        orm_mode = True


class CartAddResponse(BaseModel):
    success: bool
    cart: List[CartItem]

    class Config:
        orm_mode = True


class CartUpdateResponse(BaseModel):
    success: bool
    updated_cart: List[CartItem]

    class Config:
        orm_mode = True


class CartRemoveResponse(BaseModel):
    success: bool
    message: str

    class Config:
        orm_mode = True


class CartClearResponse(BaseModel):
    success: bool
    message: str

    class Config:
        orm_mode = True


class CartItemDetail(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float
    subtotal: float

    class Config:
        orm_mode = True

class CartTotalResponse(BaseModel):
    total: float
    item_count: int
    items: List[CartItemDetail]

    class Config:
        orm_mode = True


class CartDiscountRequest(BaseModel):
    user_id: int
    discount_code: str

class CartDiscountResponse(BaseModel):
    success: bool
    total: float
    discount_applied: float
    new_total: float
    message: Optional[str] = None

class CartSaveRequest(BaseModel):
    user_id: int


class CartSaveResponse(BaseModel):
    success: bool
    message: str

    class Config:
        orm_mode = True
#end code