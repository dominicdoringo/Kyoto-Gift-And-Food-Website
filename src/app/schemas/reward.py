# schemas/reward.py
from pydantic import BaseModel


class RewardBase(BaseModel):
    reward_tier: str
    points: int = 0


class RewardCreate(RewardBase):
    user_id: int


class RewardUpdate(BaseModel):
    points: int


class RewardRedeemRequest(BaseModel):
    user_id: int
    points: int


class Reward(BaseModel):
    user_id: int
    reward_tier: str
    points: int

    class Config:
        orm_mode = True


class RewardCreateResponse(BaseModel):
    success: bool
    message: str


class RewardUpdateResponse(BaseModel):
    success: bool
    points: int


class RewardCancelResponse(BaseModel):
    success: bool
    message: str


class RewardRedeemResponse(BaseModel):
    success: bool
    message: str
