# services/cart.py
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartRemoveResponse, CartClearResponse, CartTotalResponse, CartDiscountResponse, CartItemDetail

def get_cart_items(db: Session, user_id: int):
    cart_items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .all()
    )
    return cart_items

def add_cart_item(db: Session, item: CartItemCreate):
    if item.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be greater than zero")

    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_item = db.query(CartItem).filter(
        CartItem.user_id == item.user_id,
        CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_id=item.user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    product.stock -= item.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, user_id: int, product_id: int, item: CartItemUpdate):
    if item.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be greater than zero")

    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    quantity_difference = item.quantity - cart_item.quantity
    if quantity_difference > 0 and product.stock < quantity_difference:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Adjust stock based on quantity change
    product.stock -= quantity_difference
    cart_item.quantity = item.quantity

    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_cart_item(db: Session, user_id: int, product_id: int):
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.stock += cart_item.quantity

    db.delete(cart_item)
    db.commit()
    return CartRemoveResponse(success=True, message="Item removed from cart successfully")

def clear_cart(db: Session, user_id: int):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
        db.delete(item)
    db.commit()
    return CartClearResponse(success=True, message="Cart cleared successfully")


def get_cart_total(db: Session, user_id: int, tax_rate: float = 0.08):
    cart_items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .all()
    )
    total = 0.0
    item_count = 0
    items_details = []

    for item in cart_items:
        if item.product:
            item_total = item.product.price * item.quantity
            total += item_total
            item_count += item.quantity
            items_details.append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price,
                "subtotal": item_total
            })

    # Calculate tax
    tax = round(total * tax_rate, 2)

    # Calculate grand total
    grand_total = round(total + tax, 2)

    return CartTotalResponse(
        total=round(total, 2),
        item_count=item_count,
        items=items_details,
        tax=tax,
        grand_total=grand_total
    )


def apply_discount(db: Session, user_id: int, discount_code: str):
    
    cart_total = get_cart_total(db, user_id)
    # For simplicity, let's assume a flat 10% discount for a valid code 'SAVE10'
    if discount_code == 'SAVE10':
        discount = cart_total.total * 0.10
        new_total = cart_total.total - discount
        return CartDiscountResponse(
            success=True,
            total=cart_total.total,
            discount_applied=discount,
            new_total=new_total,
            message="Discount applied successfully."
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid discount code")
