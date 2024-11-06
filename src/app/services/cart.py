# services/cart.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate


def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


def add_cart_item(db: Session, item: CartItemCreate):
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == item.user_id,
        CartItem.product_id == item.product_id
    ).first()
    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    db_item = CartItem(
        user_id=item.user_id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_cart_item(db: Session, item_id: int, item_update: CartItemUpdate):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not cart_item:
        return None
    cart_item.quantity = item_update.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_cart_item(db: Session, item_id: int):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not cart_item:
        return False
    db.delete(cart_item)
    db.commit()
    return True


def clear_cart(db: Session, user_id: int):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        return False
    for item in cart_items:
        db.delete(item)
    db.commit()
    return True
