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

router = APIRouter()


@router.post("/", response_model=OrderCreateResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = order_service.create_order(db=db, order=order)
    return {
        "success": True,
        "order_id": db_order.id,
        "total": db_order.total,
        "status": db_order.status,
    }


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = order_service.get_order(db=db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/", response_model=list[Order])
def get_orders(user_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = order_service.get_orders(db=db, user_id=user_id, skip=skip, limit=limit)
    return orders


@router.put("/{order_id}", response_model=OrderUpdateResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = order_service.update_order(db=db, order_id=order_id, order_update=order_update)
    return {"success": True, "updated_order": updated_order}


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_service.delete_order(db=db, order_id=order_id)
    return {"detail": "Order deleted successfully"}


@router.get("/{order_id}/status/history", response_model=list[OrderStatusHistory])
def get_order_status_history(order_id: int, db: Session = Depends(get_db)):
    history = order_service.get_order_status_history(db=db, order_id=order_id)
    return history
#end code