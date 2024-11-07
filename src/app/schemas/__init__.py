# schemas/__init__.py
from .user import UserBase, UserCreate, User, UserResponse
from .product import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    Product,
    ProductResponse,
)
from .cart import (
    CartItemBase,
    CartItemCreate,
    CartItemUpdate,
    CartItem,
    CartAddResponse,
    CartUpdateResponse,
    CartRemoveResponse,
    CartClearResponse,
    CartTotalResponse,
    CartDiscountRequest,
    CartDiscountResponse,
    CartSaveRequest,
    CartSaveResponse,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "User",
    "UserResponse",
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "Product",
    "ProductResponse",
    "CartItemBase",
    "CartItemCreate",
    "CartItemUpdate",
    "CartItem",
    "CartAddResponse",
    "CartUpdateResponse",
    "CartRemoveResponse",
    "CartClearResponse",
    "CartTotalResponse",
    "CartDiscountRequest",
    "CartDiscountResponse",
    "CartSaveRequest",
    "CartSaveResponse",
]
