# models/product.py

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    featured = Column(Boolean, default=False)

    # Relationships
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
