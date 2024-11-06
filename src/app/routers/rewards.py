# app/routers/rewards.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/api/rewards", tags=["rewards"])

@router.post("/", response_model=schemas.RewardCreateResponse)
def enroll_reward(reward_create: schemas.RewardCreate, db: Session = Depends(get_db)):
    response = crud.enroll_reward(db, reward_create)
    return response

@router.get("/{userId}", response_model=schemas.Reward)
def get_reward(userId: int, db: Session = Depends(get_db)):
    reward = crud.get_reward(db, userId)
    return reward

@router.put("/{userId}", response_model=schemas.RewardUpdateResponse)
def update_reward(userId: int, reward_update: schemas.RewardUpdate, db: Session = Depends(get_db)):
    response = crud.update_reward(db, userId, reward_update.points)
    return response

@router.delete("/{userId}", response_model=schemas.RewardCancelResponse)
def cancel_reward(userId: int, db: Session = Depends(get_db)):
    response = crud.cancel_reward(db, userId)
    return response

@router.post("/{userId}/redeem", response_model=schemas.RewardRedeemResponse)
def redeem_reward(userId: int, redeem_request: schemas.RewardRedeemRequest, db: Session = Depends(get_db)):
    if userId != redeem_request.userId:
        raise HTTPException(status_code=400, detail="User ID mismatch")
    response = crud.redeem_reward(db, userId, redeem_request.points)
    return response
