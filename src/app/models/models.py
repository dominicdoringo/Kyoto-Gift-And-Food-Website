# app/models.py

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_reward_member: bool = Field(default=False)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    profile_picture_url: Optional[str] = None

    # Relationships
    reviews: List["Review"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")
    cart_items: List["CartItem"] = Relationship(back_populates="user")
    reward: Optional["Reward"] = Relationship(back_populates="user")
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    category: str
    stock: int
    featured: bool = Field(default=False)

    # Relationships
    reviews: List["Review"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")
    cart_items: List["CartItem"] = Relationship(back_populates="product")


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    user_id: int = Field(foreign_key="user.id")
    rating: int
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    product: Optional["Product"] = Relationship(back_populates="reviews")
    user: Optional["User"] = Relationship(back_populates="reviews")


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: str
    total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    status_history: List["OrderStatusHistory"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price: float

    # Relationships
    order: Optional["Order"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="order_items")


class OrderStatusHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    order: Optional["Order"] = Relationship(back_populates="status_history")


class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int

    # Relationships
    user: Optional["User"] = Relationship(back_populates="cart_items")
    product: Optional["Product"] = Relationship(back_populates="cart_items")


class Reward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    reward_tier: str
    points: int = Field(default=0)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="reward")


class RefreshToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str
    expires_at: datetime

    # Relationships
    user: Optional["User"] = Relationship(back_populates="refresh_tokens")


class SavedCart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    cart_items: str  # JSON serialized cart items

    # Relationships
    user: Optional["User"] = Relationship()
