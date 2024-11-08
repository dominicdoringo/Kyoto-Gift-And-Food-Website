# services/order.py
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderCreateResponse,
    OrderUpdateResponse,
    OrderStatusHistory,
)


def create_order(db: Session, order: OrderCreate):
    total = 0.0
    order_items = []
    for item in order.cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        product.stock -= item.quantity
        item_total = product.price * item.quantity
        total += item_total
        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        order_items.append(order_item)
    
    db_order = Order(
        user_id=order.user_id,
        payment_method=order.payment_method,
        total=total,
        items=order_items
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_orders(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(Order).options(joinedload(Order.items))
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order_update.status:
        db_order.status = order_update.status
    if order_update.shipping_address:
        db_order.shipping_address = order_update.shipping_address
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    db.delete(db_order)
    db.commit()
    return {"detail": "Order deleted successfully"}


def get_order_status_history(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Assuming there is a status history mechanism
    # Placeholder implementation
    history = [
        OrderStatusHistory(status=db_order.status, date=db_order.updated_at)
    ]
    return history
#end code