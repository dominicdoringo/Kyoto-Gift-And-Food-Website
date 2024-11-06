# app/routers/reviews.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/api/products", tags=["reviews"])

@router.post("/{id}/review", response_model=schemas.ReviewCreateResponse)
def create_review(id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    if id != review.productId:
        raise HTTPException(status_code=400, detail="Product ID mismatch")
    db_review = crud.create_review(db, review)
    return {"success": True, "review": db_review}

@router.get("/{id}/reviews", response_model=List[schemas.Review])
def get_reviews(id: int, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_by_product(db, id)
    return reviews
