# services/reward.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.reward import Reward
from app.models.user import User
from app.schemas.reward import (
    RewardCreate,
    RewardUpdate,
    RewardRedeemRequest,
)


def create_reward(db: Session, reward: RewardCreate):
    user = db.query(User).filter(User.id == reward.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.reward:
        raise HTTPException(status_code=400, detail="User is already enrolled in the rewards program")

    db_reward = Reward(
        user_id=reward.user_id,
        reward_tier=reward.reward_tier,
        points=reward.points,
    )
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward


def get_reward(db: Session, user_id: int):
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Rewards not found")
    return reward


def update_reward_points(db: Session, user_id: int, points: int):
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Rewards not found")
    reward.points = points
    db.commit()
    db.refresh(reward)
    return reward


def cancel_reward_membership(db: Session, user_id: int):
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Rewards not found")
    db.delete(reward)
    db.commit()
    return {"success": True, "message": "Rewards membership canceled successfully"}


def redeem_reward_points(db: Session, user_id: int, points: int):
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Rewards not found")
    if reward.points < points:
        raise HTTPException(status_code=400, detail="Insufficient reward points")
    reward.points -= points
    db.commit()
    db.refresh(reward)
    return {"success": True, "message": "Points redeemed successfully"}
#end code