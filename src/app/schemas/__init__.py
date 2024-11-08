# src/app/schemas/__init__.py

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserDetailResponse,
    UserLogin,
    UserProfile,
)
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
    ProductInCart,
)
from .order import (
    OrderItemBase,
    OrderItemCreate,
    OrderItem,
    OrderBase,
    OrderCreate,
    OrderUpdate,
    Order,
    OrderCreateResponse,
    OrderUpdateResponse,
    OrderStatusHistory,
)
from .reward import (
    RewardBase,
    RewardCreate,
    RewardUpdate,
    RewardRedeemRequest,
    Reward,
    RewardCreateResponse,
    RewardUpdateResponse,
    RewardCancelResponse,
    RewardRedeemResponse,
)
from .token import Token, TokenData
from .auth import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserDetailResponse",
    "UserLogin",
    "UserProfile",
    # Product schemas
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "Product",
    "ProductResponse",
    # Cart schemas
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
    "ProductInCart",
    # Order schemas
    "OrderItemBase",
    "OrderItemCreate",
    "OrderItem",
    "OrderBase",
    "OrderCreate",
    "OrderUpdate",
    "Order",
    "OrderCreateResponse",
    "OrderUpdateResponse",
    "OrderStatusHistory",
    # Reward schemas
    "RewardBase",
    "RewardCreate",
    "RewardUpdate",
    "RewardRedeemRequest",
    "Reward",
    "RewardCreateResponse",
    "RewardUpdateResponse",
    "RewardCancelResponse",
    "RewardRedeemResponse",
    # Token schemas
    "Token",
    "TokenData",
    # Auth schemas
    "LoginRequest",
    "LoginResponse",
    "TokenRefreshRequest",
    "TokenRefreshResponse",
]
