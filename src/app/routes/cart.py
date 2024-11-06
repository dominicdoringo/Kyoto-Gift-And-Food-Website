# routes/cart.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.cart as cart_service
from app.dependencies import get_db

from app.core.database import get_db
from app.schemas.cart import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
    CartClearResponse,
)
from app.models.user import User  # Assuming you have a User model


router = APIRouter()

# Add Item to Cart (POST /api/cart)
@router.post("/api/cart", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_cart_item(item: CartItemCreate, db: Session = Depends(get_db)):
    cart_item = cart_service.add_cart_item(db=db, item=item)
    if not cart_item:
        raise HTTPException(status_code=400, detail="Unable to add item to cart")
    return cart_item

# List Cart Items (GET /api/cart/{user_id})
@router.get("/api/cart/{user_id}", response_model=CartResponse)
def list_cart_items(user_id: int, db: Session = Depends(get_db)):
    cart_items = cart_service.get_cart_items(db=db, user_id=user_id)
    if cart_items is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {"items": cart_items}

# Update Cart Item Quantity (PUT /api/cart/{item_id})
@router.put("/api/cart/{item_id}", response_model=CartItemResponse)
def update_cart_item(item_id: int, item_update: CartItemUpdate, db: Session = Depends(get_db)):
    updated_item = cart_service.update_cart_item(db=db, item_id=item_id, item_update=item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item

# Remove Cart Item (DELETE /api/cart/{item_id})
@router.delete("/api/cart/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(item_id: int, db: Session = Depends(get_db)):
    success = cart_service.remove_cart_item(db=db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return

# Clear Cart (DELETE /api/cart/{user_id}/clear)
@router.delete("/api/cart/{user_id}/clear", response_model=CartClearResponse)
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    success = cart_service.clear_cart(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {"success": True, "message": "Cart cleared successfully"}
