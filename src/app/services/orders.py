# services/order.py

from sqlalchemy.orm import Session

from app.models.orders import Order
from app.models.order_item import OrderItem
from app.schemas.orders import OrderCreate, OrderUpdate
from app.schemas.order_item import OrderItemCreate

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session):
    return db.query(Order).all()

def create_order(db: Session, order: OrderCreate):
    db_order = Order(
        user_id=order.user_id,
        total_price=order.total_price,
        status=order.status,
        address=order.address
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add order items
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    db.commit()
    return db_order

def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    order = get_order(db, order_id)
    if not order:
        return None

    if order_update.status is not None:
        order.status = order_update.status
    if order_update.address is not None:
        order.address = order_update.address

    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True

def get_orders_by_user(db: Session, user_id: int):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders
