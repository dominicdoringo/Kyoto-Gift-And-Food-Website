# routes/reward.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.reward as reward_service
from app.dependencies import get_db
from app.schemas.reward import (
    RewardCreate,
    RewardUpdate,
    RewardRedeemRequest,
    Reward,
    RewardCreateResponse,
    RewardUpdateResponse,
    RewardCancelResponse,
    RewardRedeemResponse,
)

router = APIRouter()


@router.post("/", response_model=RewardCreateResponse)
def enroll_reward(reward: RewardCreate, db: Session = Depends(get_db)):
    reward_service.create_reward(db=db, reward=reward)
    return {"success": True, "message": "User enrolled in rewards program"}


@router.get("/{user_id}", response_model=Reward)
def get_reward(user_id: int, db: Session = Depends(get_db)):
    reward = reward_service.get_reward(db=db, user_id=user_id)
    return reward


@router.put("/{user_id}", response_model=RewardUpdateResponse)
def update_reward(user_id: int, reward_update: RewardUpdate, db: Session = Depends(get_db)):
    updated_reward = reward_service.update_reward_points(db=db, user_id=user_id, points=reward_update.points)
    return {"success": True, "points": updated_reward.points}


@router.delete("/{user_id}", response_model=RewardCancelResponse)
def cancel_reward(user_id: int, db: Session = Depends(get_db)):
    response = reward_service.cancel_reward_membership(db=db, user_id=user_id)
    return response


@router.post("/{user_id}/redeem", response_model=RewardRedeemResponse)
def redeem_points(user_id: int, redeem_request: RewardRedeemRequest, db: Session = Depends(get_db)):
    response = reward_service.redeem_reward_points(db=db, user_id=user_id, points=redeem_request.points)
    return response
#end code