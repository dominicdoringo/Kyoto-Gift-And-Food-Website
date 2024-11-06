from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    stock: int
    featured: Optional[bool] = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    stock: Optional[int]
    featured: Optional[bool]


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductCreateResponse(BaseModel):
    success: bool
    product: Product


class ProductUpdateResponse(BaseModel):
    success: bool
    updatedProduct: Product


class ProductInventory(BaseModel):
    id: int
    inventory: int

    class Config:
        orm_mode = True


class ProductInventoryUpdate(BaseModel):
    inventory: int


class ProductInventoryUpdateResponse(BaseModel):
    success: bool
    newInventory: int


# Review Schemas
class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    productId: int
    userId: int


class ReviewUpdate(BaseModel):
    rating: Optional[int]
    comment: Optional[str]


class Review(ReviewBase):
    id: int
    productId: int
    userId: int
    created_at: datetime

    class Config:
        orm_mode = True


class ReviewCreateResponse(BaseModel):
    success: bool
    review: Review


# Cart Schemas
class CartItem(BaseModel):
    productId: int
    quantity: int
    name: str
    price: float
    total: float

    class Config:
        orm_mode = True


class CartItemCreate(BaseModel):
    userId: int
    productId: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int


class CartAddResponse(BaseModel):
    success: bool
    cart: List[CartItem]


class CartUpdateResponse(BaseModel):
    success: bool
    updatedCart: List[CartItem]


class CartRemoveResponse(BaseModel):
    success: bool
    message: str


class CartClearResponse(BaseModel):
    success: bool
    message: str


class CartTotalResponse(BaseModel):
    total: float
    itemCount: int


class CartDiscountRequest(BaseModel):
    userId: int
    discountCode: str


class CartDiscountResponse(BaseModel):
    success: bool
    newTotal: float
    discountApplied: str


class CartSaveRequest(BaseModel):
    userId: int


class CartSaveResponse(BaseModel):
    success: bool
    message: str


# User Schemas
class UserBase(BaseModel):
    name: str
    email: str
    is_reward_member: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreateResponse(BaseModel):
    success: bool
    user: User


class UserUpdateResponse(BaseModel):
    success: bool
    updatedUser: User


class UserDeleteResponse(BaseModel):
    success: bool
    message: str


class UserDeactivateResponse(BaseModel):
    success: bool
    message: str


# Reward Schemas
class Reward(BaseModel):
    userId: int
    rewardTier: str
    points: int

    class Config:
        orm_mode = True


class RewardCreate(BaseModel):
    userId: int
    rewardTier: Optional[str]


class RewardCreateResponse(BaseModel):
    success: bool
    message: str


class RewardUpdate(BaseModel):
    points: int


class RewardUpdateResponse(BaseModel):
    success: bool
    points: int


class RewardCancelResponse(BaseModel):
    success: bool
    message: str


class RewardRedeemRequest(BaseModel):
    userId: int
    points: int


class RewardRedeemResponse(BaseModel):
    success: bool
    message: str


# Authentication Schemas
class UserLogin(BaseModel):
    email: str
    password: str


class AuthTokenResponse(BaseModel):
    success: bool
    token: str
    user: User


class TokenRefreshRequest(BaseModel):
    refreshToken: str


class TokenRefreshResponse(BaseModel):
    accessToken: str


# Order Schemas
class OrderItemBase(BaseModel):
    productId: int
    quantity: int
    price: Optional[float] = None


class OrderItem(OrderItemBase):
    price: float

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    userId: int
    paymentMethod: str
    cartItems: List[OrderItemBase]


class Order(BaseModel):
    orderId: int
    userId: int
    items: List[OrderItem]
    status: str
    total: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrderCreateResponse(BaseModel):
    success: bool
    orderId: int
    total: float
    status: str


class OrderUpdate(BaseModel):
    shippingAddress: Optional[str]
    # Add other updatable fields as needed


class OrderUpdateResponse(BaseModel):
    success: bool
    updatedOrder: Order


class OrderStatusHistory(BaseModel):
    status: str
    date: datetime

    class Config:
        orm_mode = True


# Sales Report Schema
class TopCategory(BaseModel):
    category: str
    sales: float


class SalesReport(BaseModel):
    totalSales: float
    totalOrders: int
    topCategories: List[TopCategory]

    class Config:
        orm_mode = True


# General Schemas
class ErrorResponse(BaseModel):
    success: bool = False
    message: str


# Additional Schemas
class ProfilePictureResponse(BaseModel):
    success: bool
    message: str


class DeactivateResponse(BaseModel):
    success: bool
    message: str


class PasswordChangeRequest(BaseModel):
    oldPassword: str
    newPassword: str


class PasswordChangeResponse(BaseModel):
    success: bool
    message: str
