# src/app/dependencies.py

from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


from typing import Generator

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
