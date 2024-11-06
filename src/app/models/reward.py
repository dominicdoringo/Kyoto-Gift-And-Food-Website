# models/reward.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Reward(Base):
    __tablename__ = "rewards"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    reward_tier = Column(String, nullable=False)
    points = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="reward")
