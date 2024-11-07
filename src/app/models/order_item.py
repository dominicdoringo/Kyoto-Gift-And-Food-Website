# models/order_item.py

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
