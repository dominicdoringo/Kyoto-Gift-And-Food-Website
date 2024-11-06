# app/routers/cart.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/", response_model=List[schemas.CartItem])
def get_cart_items(userId: int, db: Session = Depends(get_db)):
    cart_items = crud.get_cart_items(db, userId)
    return cart_items

@router.post("/", response_model=schemas.CartAddResponse)
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    response = crud.add_to_cart(db, cart_item)
    return response

@router.delete("/", response_model=schemas.CartClearResponse)
def clear_cart(userId: int, db: Session = Depends(get_db)):
    response = crud.clear_cart(db, userId)
    return response

@router.put("/{productId}", response_model=schemas.CartUpdateResponse)
def update_cart_item(productId: int, cart_item_update: schemas.CartItemUpdate, userId: int, db: Session = Depends(get_db)):
    response = crud.update_cart_item(db, userId, productId, cart_item_update.quantity)
    return {"success": True, "updatedCart": response}

@router.delete("/{productId}", response_model=schemas.CartRemoveResponse)
def remove_cart_item(productId: int, userId: int, db: Session = Depends(get_db)):
    response = crud.remove_cart_item(db, userId, productId)
    return response

@router.get("/total", response_model=schemas.CartTotalResponse)
def get_cart_total(userId: int, db: Session = Depends(get_db)):
    total_response = crud.get_cart_total(db, userId)
    return total_response
