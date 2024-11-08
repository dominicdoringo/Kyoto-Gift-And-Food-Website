# routes/cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.services.cart as cart_service
from app.dependencies import get_db
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartRemoveResponse,
    CartClearResponse,
    CartTotalResponse,
    CartAddResponse,
    CartUpdateResponse,
    CartItem,
)
from app.core.auth import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()


@router.get("/", response_model=List[CartItem], tags=["Cart"])
def get_cart_items(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    cart_items = cart_service.get_cart_items(db, user_id=current_user.id)
    return cart_items


@router.post("/", response_model=CartAddResponse, tags=["Cart"])
def add_cart_item(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item.user_id = current_user.id
    cart_service.add_cart_item(db=db, item=item)
    cart_items = cart_service.get_cart_items(db, user_id=current_user.id)
    return {"success": True, "cart": cart_items}


@router.put("/{product_id}", response_model=CartUpdateResponse, tags=["Cart"])
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_service.update_cart_item(db=db, user_id=current_user.id, product_id=product_id, item=item)
    cart_items = cart_service.get_cart_items(db, user_id=current_user.id)
    return {"success": True, "updated_cart": cart_items}


@router.delete("/{product_id}", response_model=CartRemoveResponse, tags=["Cart"])
def remove_cart_item(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    response = cart_service.remove_cart_item(db=db, user_id=current_user.id, product_id=product_id)
    return response


@router.delete("/", response_model=CartClearResponse, tags=["Cart"])
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    response = cart_service.clear_cart(db=db, user_id=current_user.id)
    return response


@router.get("/total", response_model=CartTotalResponse, tags=["Cart"])
def get_cart_total(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total = cart_service.get_cart_total(db=db, user_id=current_user.id)
    return total
