# routes/orders.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.orders as order_service
from app.dependencies import get_db
from app.schemas.orders import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)
from app.models.orders import Order

router = APIRouter()

# Create a New Order (POST /api/orders)
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = order_service.create_order(db=db, order=order)
    if not new_order:
        raise HTTPException(status_code=400, detail="Unable to create order")
    return new_order

# List All Orders (GET /api/orders)
@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    orders = order_service.get_all_orders(db=db)
    return orders

# Get Order Details by ID (GET /api/orders/{id})
@router.get("/{id}", response_model=OrderResponse)
def get_order_by_id(id: int, db: Session = Depends(get_db)):
    order = order_service.get_order(db=db, order_id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Update Order Information (PUT /api/orders/{id})
@router.put("/{id}", response_model=OrderResponse)
def update_order(
    id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
):
    updated_order = order_service.update_order(db=db, order_id=id, order_update=order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

# Delete an Order (DELETE /api/orders/{id})
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, db: Session = Depends(get_db)):
    success = order_service.delete_order(db=db, order_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return

# Get Orders by User ID (GET /api/users/{user_id}/orders)
@router.get("/user/{user_id}", response_model=List[OrderResponse])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = order_service.get_orders_by_user(db=db, user_id=user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders
