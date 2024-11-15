# models/order.py
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, default="pending", nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    subtotal = Column(Numeric(10, 2), nullable=False)  # Adjust precision and scale as needed
    tax = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)  # Adjust precision and scale as needed
    tax = Column(Numeric(10, 2), nullable=False)


    order = relationship("Order", back_populates="items")
    product = relationship("Product")
#end code