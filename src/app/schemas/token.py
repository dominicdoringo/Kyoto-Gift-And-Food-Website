# schemas/token.py
from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime  

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str | None = None


class TokenCreate(BaseModel):
    user_id: int
    token_type: str
    token: str
    expires_at: datetime
