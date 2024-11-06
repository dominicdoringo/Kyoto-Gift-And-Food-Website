# models/user.py

from datetime import datetime, timezone
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # Simplified admin representation
    is_reward_member = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    reward = relationship("Reward", back_populates="user", uselist=False)
    auth_tokens = relationship("AuthToken", back_populates="user")
