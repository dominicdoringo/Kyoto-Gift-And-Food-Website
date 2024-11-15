from fastapi import APIRouter, Depends
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
    CartDiscountResponse,
    CartDiscountRequest,
)
from typing import List

router = APIRouter()


@router.get("/", response_model=List[CartItem])
def get_cart_items(user_id: int, db: Session = Depends(get_db)):
    cart_items = cart_service.get_cart_items(db, user_id=user_id)
    return cart_items


@router.post("/", response_model=CartAddResponse)
def add_cart_item(item: CartItemCreate, db: Session = Depends(get_db)):
    cart_service.add_cart_item(db=db, item=item)
    cart_items = cart_service.get_cart_items(db, user_id=item.user_id)
    return {"success": True, "cart": cart_items}


@router.put("/{product_id}", response_model=CartUpdateResponse)
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    cart_service.update_cart_item(db=db, user_id=user_id, product_id=product_id, item=item)
    cart_items = cart_service.get_cart_items(db, user_id=user_id)
    return {"success": True, "updated_cart": cart_items}


@router.delete("/{product_id}", response_model=CartRemoveResponse)
def remove_cart_item(product_id: int, user_id: int, db: Session = Depends(get_db)):
    response = cart_service.remove_cart_item(db=db, user_id=user_id, product_id=product_id)
    return response


@router.delete("/", response_model=CartClearResponse)
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    response = cart_service.clear_cart(db=db, user_id=user_id)
    return response


@router.get("/total", response_model=CartTotalResponse)
def get_cart_total(user_id: int, db: Session = Depends(get_db), tax_rate: float = 0.08):
    total = cart_service.get_cart_total(db=db, user_id=user_id, tax_rate=tax_rate)
    return total


@router.post("/discount", response_model=CartDiscountResponse)
def apply_discount(request: CartDiscountRequest, db: Session = Depends(get_db)):
    return cart_service.apply_discount(db=db, user_id=request.user_id, discount_code=request.discount_code)
