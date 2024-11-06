# app/routers/orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderCreateResponse)
def create_order(order_create: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, order_create)
    return {
        "success": True,
        "orderId": db_order.id,
        "total": db_order.total,
        "status": db_order.status
    }

@router.get("/", response_model=List[schemas.Order])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/{orderId}", response_model=schemas.Order)
def get_order(orderId: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, orderId)
    return order

@router.put("/{orderId}", response_model=schemas.OrderUpdateResponse)
def update_order(orderId: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    updated_order = crud.update_order(db, orderId, order_update)
    return {"success": True, "updatedOrder": updated_order}

@router.delete("/{orderId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(orderId: int, db: Session = Depends(get_db)):
    crud.delete_order(db, orderId)
    return

@router.get("/{orderId}/status/history", response_model=List[schemas.OrderStatusHistory])
def get_order_status_history(orderId: int, db: Session = Depends(get_db)):
    status_history = crud.get_order_status_history(db, orderId)
    return status_history
