# tests/test_cart.py

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

def test_add_cart_item_existing_cart_item(client, db):
    """
    Test adding a product that's already in the cart, ensuring the quantity updates correctly.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 1", 50)
    clear_user_cart(db, "test_cart_user")

    # Get user and product
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product = db.query(Product).filter(Product.name == "Cart Test Product 1").first()

    # First addition
    response1 = client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 1
        }
    )
    assert response1.status_code == 200
    data1 = response1.json()
    cart_item1 = data1["cart"][0]
    assert cart_item1["quantity"] == 1

    # Second addition
    response2 = client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 3
        }
    )
    assert response2.status_code == 200
    data2 = response2.json()
    cart_item2 = data2["cart"][0]
    assert cart_item2["quantity"] == 4  # Quantity should be updated to 4

    # Verify stock reduction
    db.refresh(product)
    assert product.stock == 50 - 4

def test_get_cart_items(client, db):
    """
    Test retrieving all cart items for a user.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 1", 50)
    reset_product_stock(db, "Cart Test Product 2", 30)
    clear_user_cart(db, "test_cart_user")

    # Get user and products
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product1 = db.query(Product).filter(Product.name == "Cart Test Product 1").first()
    product2 = db.query(Product).filter(Product.name == "Cart Test Product 2").first()

    # Add items to cart
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product1.id,
            "quantity": 2
        }
    )
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product2.id,
            "quantity": 1
        }
    )

    response = client.get(f"/cart/?user_id={user.id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    product_ids_in_cart = [item["product"]["id"] for item in data]
    assert product1.id in product_ids_in_cart
    assert product2.id in product_ids_in_cart

def test_update_cart_item_success(client, db):
    """
    Test updating the quantity of an existing cart item successfully.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 2", 30)
    clear_user_cart(db, "test_cart_user")

    # Get user and product
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product = db.query(Product).filter(Product.name == "Cart Test Product 2").first()

    # Add item to cart
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 2
        }
    )

    # Update the cart item
    response = client.put(
        f"/cart/{product.id}",
        json={
            "quantity": 5
        },
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    updated_item = next((item for item in data["updated_cart"] if item["product"]["id"] == product.id), None)
    assert updated_item is not None
    assert updated_item["quantity"] == 5

    # Verify stock reduction
    db.refresh(product)
    assert product.stock == 30 - 5

def test_update_cart_item_insufficient_stock(client, db):
    """
    Test updating a cart item to a quantity that exceeds available stock.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 3", 20)
    clear_user_cart(db, "test_cart_user")

    # Get user and product
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product = db.query(Product).filter(Product.name == "Cart Test Product 3").first()

    # Add item to cart
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 5
        }
    )

    # Attempt to update to a quantity exceeding stock
    response = client.put(
        f"/cart/{product.id}",
        json={
            "quantity": 25
        },
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Insufficient stock"

def test_remove_cart_item_success(client, db):
    """
    Test removing an existing item from the cart successfully.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 1", 50)
    clear_user_cart(db, "test_cart_user")

    # Get user and product
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product = db.query(Product).filter(Product.name == "Cart Test Product 1").first()

    # Add item to cart
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product.id,
            "quantity": 3
        }
    )

    # Remove the cart item
    response = client.delete(
        f"/cart/{product.id}",
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Item removed from cart successfully"

    # Verify stock restoration
    db.refresh(product)
    assert product.stock == 50  # Original stock

    # Verify cart is empty
    response = client.get(f"/cart/?user_id={user.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_remove_cart_item_not_found(client, db):
    """
    Test removing a cart item that does not exist.
    """
    # Reset state
    clear_user_cart(db, "test_cart_user")

    # Get user
    user = db.query(User).filter(User.username == "test_cart_user").first()

    nonexistent_product_id = 88888  # Assuming this ID doesn't exist in cart

    # Attempt to remove cart item
    response = client.delete(
        f"/cart/{nonexistent_product_id}",
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Cart item not found"

def test_clear_cart_success(client, db):
    """
    Test clearing the cart successfully.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 1", 50)
    reset_product_stock(db, "Cart Test Product 2", 30)
    clear_user_cart(db, "test_cart_user")

    # Get user and products
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product1 = db.query(Product).filter(Product.name == "Cart Test Product 1").first()
    product2 = db.query(Product).filter(Product.name == "Cart Test Product 2").first()

    # Add items to cart
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product1.id,
            "quantity": 2
        }
    )
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product2.id,
            "quantity": 1
        }
    )

    # Clear the cart
    response = client.delete(
        "/cart/",
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Cart cleared successfully"

    # Verify cart is empty
    response = client.get(f"/cart/?user_id={user.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

    # Verify stock restoration
    db.refresh(product1)
    db.refresh(product2)
    assert product1.stock == 50
    assert product2.stock == 30

def test_get_cart_total(client, db):
    """
    Test calculating the total price and item count in the cart.
    """
    # Reset state
    reset_product_stock(db, "Cart Test Product 1", 50)
    reset_product_stock(db, "Cart Test Product 2", 30)
    clear_user_cart(db, "test_cart_user")

    # Get user and products
    user = db.query(User).filter(User.username == "test_cart_user").first()
    product1 = db.query(Product).filter(Product.name == "Cart Test Product 1").first()
    product2 = db.query(Product).filter(Product.name == "Cart Test Product 2").first()

    # Add items to cart
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product1.id,
            "quantity": 3  # 3 * $10 = $30
        }
    )
    client.post(
        "/cart/",
        json={
            "user_id": user.id,
            "product_id": product2.id,
            "quantity": 2  # 2 * $20 = $40
        }
    )

    # Get cart total
    response = client.get(
        "/cart/total",
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 70.0
    assert data["item_count"] == 5

def test_get_cart_total_empty_cart(client, db):
    """
    Test calculating the total price and item count for an empty cart.
    """
    # Reset state
    clear_user_cart(db, "test_cart_user")

    # Get user
    user = db.query(User).filter(User.username == "test_cart_user").first()

    # Get cart total
    response = client.get(
        "/cart/total",
        params={
            "user_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0.0
    assert data["item_count"] == 0

