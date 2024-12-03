# models/reward.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    reward_tier = Column(String, nullable=False)
    points = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="reward")
