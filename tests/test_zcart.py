# tests/test_zcart.py

import pytest
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User

def reset_product_stock(db, product_name, stock):
    product = db.query(Product).filter(Product.name == product_name).first()
    assert product is not None, f"Product {product_name} not found"
    product.stock = stock
    db.commit()
    db.refresh(product)

def clear_user_cart(db, username):
    user = db.query(User).filter(User.username == username).first()
    assert user is not None, f"User {username} not found"
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()

def test_add_cart_item_success(client, db):
    # Reset state
    reset_product_stock(db, "Cart Test Product 1", 50)
    clear_user_cart(db, "test_cart_user")

    # Get user and product
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product = db.query(Product).filter(Product.name == "Cart Test Product 1").first()
    initial_stock = product.stock

    response = client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["cart"]) == 1
    cart_item = data["cart"][0]
    assert cart_item["product"]["id"] == product.id
    assert cart_item["quantity"] == 2

    # Verify stock reduction
    db.refresh(product)
    assert product.stock == initial_stock - 2

def test_add_cart_item_nonexistent_product(client, db):
    # Reset state
    clear_user_cart(db, "test_cart_user")

    # Get user
    user = db.query(User).filter(User.username == "test_cart_user").first()

    nonexistent_product_id = 99999  # Assuming this ID doesn't exist

    response = client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": nonexistent_product_id,
            "quantity": 1
        }
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"

# Continue adjusting the rest of the test functions similarly...

def test_add_cart_item_insufficient_stock(client, db):
    # Reset state
    reset_product_stock(db, "Cart Test Product 3", 20)
    clear_user_cart(db, "test_cart_user")

    # Get user and product
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product = db.query(Product).filter(Product.name == "Cart Test Product 3").first()

    response = client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 25  # Exceeds stock
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Insufficient stock"

# Continue with the rest of your tests, resetting state at the beginning of each.
