# src/app/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.services.user as user_service
import app.services.order as order_service
from app.core.auth import get_admin_user
from app.core.auth import get_current_user
from app.dependencies import get_db
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserUpdateResponse,
)
from app.schemas.order import (
    Order,
    OrderCreateResponse,
    OrderUpdateResponse,
    OrderStatusHistory,
    OrderUpdate,
)
from app.models.user import User

router = APIRouter()


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_all_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: List all users.
    """
    users = user_service.list_users(db=db, current_user=admin_user)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_details_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Get user details by ID.
    """
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserUpdateResponse)
def update_user_info_admin(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Update any user's information.
    """
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = user_service.update_user_admin(db=db, user_id=user_id, user_update=user_update)
    return updated_user


@router.delete("/users/{user_id}", status_code=204)
def delete_user_account_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Delete any user account.
    """
    user_service.delete_user_admin(db=db, user_id=user_id)
    return

# ================== Admin Order Service Functions ==================

@router.get("/orders", response_model=List[Order])
def list_all_orders(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: List all orders in the system.
    """
    orders = order_service.list_all_orders(db=db)
    return orders


@router.get("/orders/{order_id}", response_model=Order)
def get_order_details_admin(
    order_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Get details of any order by ID.
    """
    order = order_service.get_order_by_id(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=OrderUpdateResponse)
def update_order_admin(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Update any order's information.
    """
    updated_order = order_service.update_order_admin(
        db=db,
        order_id=order_id,
        order_update=order_update
    )
    return {"success": True, "updated_order": updated_order}


@router.delete("/orders/{order_id}", status_code=204)
def delete_order_admin(
    order_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Delete any order.
    """
    order_service.delete_order_admin(
        db=db,
        order_id=order_id
    )
    return