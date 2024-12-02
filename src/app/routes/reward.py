# routes/reward.py
from fastapi import APIRouter, Depends, HTTPException
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
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=RewardCreateResponse)
def enroll_reward(
    reward: RewardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reward_service.create_reward(db=db, user_id=current_user.id, reward=reward)
    return {"success": True, "message": "User enrolled in rewards program"}


@router.get("/", response_model=Reward)
def get_reward(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reward = reward_service.get_reward(db=db, user_id=current_user.id)
    return reward


@router.put("/", response_model=RewardUpdateResponse)
def update_reward(
    reward_update: RewardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_reward = reward_service.update_reward_points(
        db=db, user_id=current_user.id, points=reward_update.points
    )
    return {"success": True, "points": updated_reward.points}


@router.delete("/", response_model=RewardCancelResponse)
def cancel_reward(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = reward_service.cancel_reward_membership(db=db, user_id=current_user.id)
    return response


@router.post("/redeem", response_model=RewardRedeemResponse)
def redeem_points(
    redeem_request: RewardRedeemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = reward_service.redeem_reward_points(
        db=db, user_id=current_user.id, points=redeem_request.points
    )
    return response
