# app/routers/admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/reports/sales", response_model=schemas.SalesReport)
def get_sales_report(startDate: str, endDate: str, db: Session = Depends(get_db)):
    # Parse the date strings
    try:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    report = crud.get_sales_report(db, start_date, end_date)
    return report

@router.get("/users", response_model=List[schemas.User])
def list_users_admin(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{id}", response_model=schemas.User)
def get_user_admin(id: int, db: Session = Depends(get_db)):
    user = crud.get_user_details_admin(db, id)
    return user

@router.delete("/users/{id}", response_model=schemas.UserDeleteResponse)
def delete_user_admin(id: int, db: Session = Depends(get_db)):
    response = crud.delete_user_admin(db, id)
    return response

@router.put("/users/{id}/deactivate", response_model=schemas.UserDeactivateResponse)
def deactivate_user_admin(id: int, db: Session = Depends(get_db)):
    response = crud.deactivate_user_admin(db, id)
    return response
