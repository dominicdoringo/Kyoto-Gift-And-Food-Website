from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderStatusHistory,
)
from app.services.cart import get_cart_items, clear_cart  # Import cart services


def create_order(db: Session, user_id: int, order: OrderCreate, tax_rate: float = 0.08):
    # Fetch cart items for the current user
    cart_items = get_cart_items(db, user_id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    subtotal = 0.0
    total_tax = 0.0
    order_items = []

    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {cart_item.product_id} not found")
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {product.name}"
            )
        product.stock -= cart_item.quantity

        # Calculate per-item subtotal and tax
        item_subtotal = product.price * cart_item.quantity
        item_tax = round(item_subtotal * tax_rate, 2)
        item_total = round(item_subtotal + item_tax, 2)

        subtotal += item_subtotal
        total_tax += item_tax

        order_item = OrderItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product.price,
            subtotal=item_subtotal,
            tax=item_tax
        )
        order_items.append(order_item)

    # Calculate grand total
    total = round(subtotal + total_tax, 2)

    db_order = Order(
        user_id=user_id,
        payment_method=order.payment_method,
        status="pending",
        subtotal=subtotal,
        tax=total_tax,
        total=total,
        items=order_items
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Clear the cart after creating the order
    clear_cart(db, user_id)

    return db_order




def get_order(db: Session, user_id: int, order_id: int):
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    orders = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders


def update_order(db: Session, user_id: int, order_id: int, order_update: OrderUpdate):
    db_order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order_update.status:
        db_order.status = order_update.status
    if order_update.shipping_address:
        db_order.shipping_address = order_update.shipping_address
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, user_id: int, order_id: int):
    db_order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    db.delete(db_order)
    db.commit()
    return {"detail": "Order deleted successfully"}


def get_order_status_history(db: Session, user_id: int, order_id: int):
    db_order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Placeholder implementation for status history
    history = [
        OrderStatusHistory(status=db_order.status, date=db_order.updated_at)
    ]
    return history
