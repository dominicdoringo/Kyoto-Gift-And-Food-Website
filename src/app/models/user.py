# src/app/models/user.py
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    cart_items = relationship(
        "CartItem", back_populates="user", cascade="all, delete-orphan"
    )
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reward = relationship("Reward", back_populates="user", uselist=False)
