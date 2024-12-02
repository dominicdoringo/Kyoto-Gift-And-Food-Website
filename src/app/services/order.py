from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload 
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderStatusHistory,
)
from app.services.cart import get_cart_items, clear_cart
from app.services.reward import calculate_reward_points, update_reward_points

from decimal import Decimal, ROUND_HALF_UP, getcontext

# Set the precision and rounding
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP

def create_order(db: Session, user_id: int, order: OrderCreate, tax_rate: float = 0.08):
    try:
        # Fetch cart items for the current user
        cart_items = get_cart_items(db, user_id)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        subtotal = Decimal('0.00')
        total_tax = Decimal('0.00')
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

            # Convert values to Decimal
            price = Decimal(str(product.price))
            quantity = Decimal(str(cart_item.quantity))
            tax_rate_decimal = Decimal(str(tax_rate))

            # Calculate per-item subtotal and tax with Decimal
            item_subtotal = (price * quantity).quantize(Decimal('0.01'))
            item_tax = (item_subtotal * tax_rate_decimal).quantize(Decimal('0.01'))
            item_total = (item_subtotal + item_tax).quantize(Decimal('0.01'))

            subtotal += item_subtotal
            total_tax += item_tax

            order_item = OrderItem(
                product_id=cart_item.product_id,
                quantity=int(quantity),
                price=float(price),
                subtotal=float(item_subtotal),
                tax=float(item_tax)
            )
            order_items.append(order_item)

        # Calculate grand total
        total = (subtotal + total_tax).quantize(Decimal('0.01'))

        db_order = Order(
            user_id=user_id,
            payment_method=order.payment_method,
            status="pending",
            subtotal=float(subtotal),
            tax=float(total_tax),
            total=float(total),
            items=order_items
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Calculate reward points based on the total amount
        reward_points = calculate_reward_points(float(total))
        if reward_points > 0:
            # Update user's reward points
            update_reward_points(db, user_id, reward_points)

        # Clear the cart after creating the order
        clear_cart(db, user_id)

        return db_order
    except Exception as e:
        db.rollback()
        raise e




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
        .options(joinedload(Order.items).joinedload(OrderItem.product))
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
