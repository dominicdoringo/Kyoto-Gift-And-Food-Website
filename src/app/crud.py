# app/crud.py

from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app import models
from app.schemas import UserCreate  # Import UserCreate directly
from app import schemas

# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ------------------- User CRUD Operations -------------------

def get_user(db: Session, user_id: int):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(db: Session, user: UserCreate):
    existing_user = db.exec(select(models.User).where(models.User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_reward_member=user.is_reward_member,
        is_active=True,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




# ------------------- Product CRUD Operations -------------------

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    products = db.exec(select(models.Product).offset(skip).limit(limit)).all()
    return products

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    product = get_product(db, product_id)
    product_data = product_update.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"success": True, "message": "Product deleted successfully"}

def search_products(db: Session, query: str):
    products = db.exec(select(models.Product).where(models.Product.name.contains(query))).all()
    return products

def get_products_by_category(db: Session, category_name: str):
    products = db.exec(select(models.Product).where(models.Product.category == category_name)).all()
    if not products:
        raise HTTPException(status_code=404, detail="Category not found")
    return products

def filter_products_by_price(db: Session, min_price: float, max_price: float):
    products = db.exec(
        select(models.Product).where(
            models.Product.price >= min_price,
            models.Product.price <= max_price
        )
    ).all()
    return products

def get_featured_products(db: Session):
    products = db.exec(select(models.Product).where(models.Product.featured == True)).all()
    return products

def get_product_inventory(db: Session, product_id: int):
    product = get_product(db, product_id)
    return schemas.ProductInventory(id=product.id, inventory=product.stock)

def update_product_inventory(db: Session, product_id: int, inventory: int):
    product = get_product(db, product_id)
    product.stock = inventory
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"success": True, "newInventory": product.stock}

# ------------------- Review CRUD Operations -------------------

def create_review(db: Session, review: schemas.ReviewCreate):
    product = get_product(db, review.productId)
    user = get_user(db, review.userId)
    db_review = models.Review(
        product_id=product.id,
        user_id=user.id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    return product.reviews

# ------------------- Cart CRUD Operations -------------------

def add_to_cart(db: Session, cart_item: schemas.CartItemCreate):
    user = get_user(db, cart_item.userId)
    product = get_product(db, cart_item.productId)
    existing_cart_item = db.exec(
        select(models.CartItem).where(
            models.CartItem.user_id == user.id,
            models.CartItem.product_id == product.id
        )
    ).first()
    if existing_cart_item:
        existing_cart_item.quantity += cart_item.quantity
        db.add(existing_cart_item)
    else:
        db_cart_item = models.CartItem(
            user_id=user.id,
            product_id=product.id,
            quantity=cart_item.quantity
        )
        db.add(db_cart_item)
    db.commit()
    return {"success": True, "message": "Item added to cart"}

def get_cart_items(db: Session, user_id: int):
    user = get_user(db, user_id)
    cart_items = db.exec(
        select(models.CartItem).where(models.CartItem.user_id == user.id)
    ).all()
    return cart_items

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    cart_item = db.exec(
        select(models.CartItem).where(
            models.CartItem.user_id == user_id,
            models.CartItem.product_id == product_id
        )
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart_item.quantity = quantity
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"success": True, "message": "Cart item updated"}

def remove_cart_item(db: Session, user_id: int, product_id: int):
    cart_item = db.exec(
        select(models.CartItem).where(
            models.CartItem.user_id == user_id,
            models.CartItem.product_id == product_id
        )
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"success": True, "message": "Item removed from cart"}

def clear_cart(db: Session, user_id: int):
    cart_items = db.exec(
        select(models.CartItem).where(models.CartItem.user_id == user_id)
    ).all()
    for item in cart_items:
        db.delete(item)
    db.commit()
    return {"success": True, "message": "Cart cleared"}

def get_cart_total(db: Session, user_id: int):
    cart_items = get_cart_items(db, user_id)
    total = 0.0
    item_count = 0
    for item in cart_items:
        product = get_product(db, item.product_id)
        total += product.price * item.quantity
        item_count += item.quantity
    return schemas.CartTotalResponse(total=total, itemCount=item_count)

# Placeholder functions for discount and save cart (business logic required)

# ------------------- Order CRUD Operations -------------------

def create_order(db: Session, order_create: schemas.OrderCreate):
    user = get_user(db, order_create.userId)
    cart_items = order_create.cartItems
    order_items = []
    total = 0.0

    for item in cart_items:
        product = get_product(db, item.productId)
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
        order_item = models.OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        order_items.append(order_item)
        product.stock -= item.quantity
        db.add(product)
        total += product.price * item.quantity

    db_order = models.Order(
        user_id=user.id,
        status="Pending",
        total=total,
        items=order_items
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    order = db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    orders = db.exec(select(models.Order).offset(skip).limit(limit)).all()
    return orders

def update_order(db: Session, order_id: int, order_update: schemas.OrderUpdate):
    order = get_order(db, order_id)
    order_data = order_update.dict(exclude_unset=True)
    for key, value in order_data.items():
        setattr(order, key, value)
    order.updated_at = datetime.utcnow()
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    db.delete(order)
    db.commit()
    return {"success": True, "message": "Order canceled"}

def get_order_status_history(db: Session, order_id: int):
    order = get_order(db, order_id)
    return order.status_history

# ------------------- Reward CRUD Operations -------------------

def enroll_reward(db: Session, reward_create: schemas.RewardCreate):
    user = get_user(db, reward_create.userId)
    if user.is_reward_member:
        raise HTTPException(status_code=400, detail="User already enrolled")
    db_reward = models.Reward(
        user_id=user.id,
        reward_tier=reward_create.rewardTier or "Bronze",
        points=0
    )
    user.is_reward_member = True
    db.add(db_reward)
    db.add(user)
    db.commit()
    db.refresh(db_reward)
    return {"success": True, "message": "User enrolled in rewards program"}

def get_reward(db: Session, user_id: int):
    reward = db.exec(select(models.Reward).where(models.Reward.user_id == user_id)).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Rewards not found")
    return reward

def update_reward(db: Session, user_id: int, points: int):
    reward = get_reward(db, user_id)
    reward.points += points
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return {"success": True, "points": reward.points}

def cancel_reward(db: Session, user_id: int):
    reward = get_reward(db, user_id)
    user = get_user(db, user_id)
    db.delete(reward)
    user.is_reward_member = False
    db.add(user)
    db.commit()
    return {"success": True, "message": "Rewards membership canceled"}

def redeem_reward(db: Session, user_id: int, points: int):
    reward = get_reward(db, user_id)
    if reward.points < points:
        raise HTTPException(status_code=400, detail="Insufficient points")
    reward.points -= points
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return {"success": True, "message": f"{points} points redeemed"}

# ------------------- Authentication Functions -------------------

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Placeholder for token generation and refresh functions

def get_user_by_email(db: Session, email: str):
    user = db.exec(select(models.User).where(models.User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ------------------- Admin Functions -------------------

def get_sales_report(db: Session, start_date: datetime, end_date: datetime):
    # Placeholder for sales report logic
    pass

def get_user_details_admin(db: Session, user_id: int):
    user = get_user(db, user_id)
    return user

def deactivate_user_admin(db: Session, user_id: int):
    user = get_user(db, user_id)
    user.is_active = False
    db.add(user)
    db.commit()
    return {"success": True, "message": "User account deactivated"}

def delete_user_admin(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return {"success": True, "message": "User deleted successfully"}
