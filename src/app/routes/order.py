# routes/order.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.services.order as order_service
from app.dependencies import get_db
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    Order,
    OrderCreateResponse,
    OrderUpdateResponse,
    OrderStatusHistory,
)
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=OrderCreateResponse)
def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order.user_id = current_user.id
    db_order = order_service.create_order(db=db, order=order)
    return {
        "success": True,
        "order_id": db_order.id,
        "total": db_order.total,
        "status": db_order.status,
    }


@router.get("/{order_id}", response_model=Order)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_order = order_service.get_order(db=db, order_id=order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/", response_model=list[Order])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = order_service.get_orders(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return orders


@router.put("/{order_id}", response_model=OrderUpdateResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_order = order_service.get_order(db=db, order_id=order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    updated_order = order_service.update_order(db=db, order_id=order_id, order_update=order_update)
    return {"success": True, "updated_order": updated_order}


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_order = order_service.get_order(db=db, order_id=order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    order_service.delete_order(db=db, order_id=order_id)
    return {"detail": "Order deleted successfully"}


@router.get("/{order_id}/status/history", response_model=list[OrderStatusHistory])
def get_order_status_history(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_order = order_service.get_order(db=db, order_id=order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    history = order_service.get_order_status_history(db=db, order_id=order_id)
    return history
