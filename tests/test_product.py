# tests/test_products.py

import pytest
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def test_create_product_success(client, db):
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A product for testing",
            "price": 19.99,
            "category": "Test Category",
            "stock": 100,
            "featured": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    product = data["product"]
    assert product["name"] == "Test Product"
    assert product["description"] == "A product for testing"
    assert product["price"] == 19.99
    assert product["category"] == "Test Category"
    assert product["stock"] == 100
    assert product["featured"] is True
    assert "id" in product
    assert "created_at" in product

def test_create_product_duplicate(client, db):
    # First creation should succeed
    response = client.post(
        "/products/",
        json={
            "name": "Duplicate Product",
            "description": "First instance",
            "price": 29.99,
            "category": "Duplicate Category",
            "stock": 50,
            "featured": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Second creation with the same name should fail
    response = client.post(
        "/products/",
        json={
            "name": "Duplicate Product",
            "description": "Second instance",
            "price": 39.99,
            "category": "Duplicate Category",
            "stock": 30,
            "featured": False
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Product already exists"

def test_get_products(client, db):
    # Ensure there are some products in the database
    products = db.query(Product).all()
    initial_count = len(products)

    # Create additional products
    client.post(
        "/products/",
        json={
            "name": "Product 1",
            "description": "Description 1",
            "price": 10.0,
            "category": "Category A",
            "stock": 20,
            "featured": False
        }
    )
    client.post(
        "/products/",
        json={
            "name": "Product 2",
            "description": "Description 2",
            "price": 20.0,
            "category": "Category B",
            "stock": 30,
            "featured": True
        }
    )

    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= initial_count + 2  # At least two new products
    for product in data:
        assert "id" in product
        assert "name" in product
        assert "price" in product

def test_get_product_by_id_success(client, db):
    # Create a product to fetch
    response = client.post(
        "/products/",
        json={
            "name": "Fetchable Product",
            "description": "To be fetched",
            "price": 49.99,
            "category": "Fetch Category",
            "stock": 10,
            "featured": False
        }
    )
    assert response.status_code == 200
    product = response.json()["product"]

    # Fetch the product by ID
    response = client.get(f"/products/{product['id']}")
    assert response.status_code == 200
    fetched_product = response.json()
    assert fetched_product["id"] == product["id"]
    assert fetched_product["name"] == "Fetchable Product"

def test_get_product_by_id_not_found(client, db):
    response = client.get("/products/99999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"

def test_update_product_success(client, db):
    # Create a product to update
    response = client.post(
        "/products/",
        json={
            "name": "Updatable Product",
            "description": "Original Description",
            "price": 59.99,
            "category": "Original Category",
            "stock": 15,
            "featured": False
        }
    )
    assert response.status_code == 200
    product = response.json()["product"]

    # Update the product
    response = client.put(
        f"/products/{product['id']}",
        json={
            "description": "Updated Description",
            "price": 69.99,
            "stock": 25
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    updated_product = data["product"]
    assert updated_product["description"] == "Updated Description"
    assert updated_product["price"] == 69.99
    assert updated_product["stock"] == 25
    # Ensure other fields remain unchanged
    assert updated_product["name"] == "Updatable Product"
    assert updated_product["category"] == "Original Category"
    assert updated_product["featured"] is False

def test_update_product_not_found(client, db):
    response = client.put(
        "/products/99999",  # Assuming this ID doesn't exist
        json={
            "description": "Should not work",
            "price": 99.99
        }
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"

def test_delete_product_success(client, db):
    # Create a product to delete
    response = client.post(
        "/products/",
        json={
            "name": "Deletable Product",
            "description": "To be deleted",
            "price": 39.99,
            "category": "Delete Category",
            "stock": 5,
            "featured": False
        }
    )
    assert response.status_code == 200
    product = response.json()["product"]

    # Delete the product
    response = client.delete(f"/products/{product['id']}")
    assert response.status_code == 200  # Since the route returns a dict
    data = response.json()
    assert data["detail"] == "Product deleted successfully"

    # Verify the product is deleted
    response = client.get(f"/products/{product['id']}")
    assert response.status_code == 404

def test_delete_product_not_found(client, db):
    response = client.delete("/products/99999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"

def test_invalid_product_creation(client, db):
    # Missing required fields (e.g., price)
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "description": "Missing price",
            "category": "Invalid Category",
            "stock": 10,
            "featured": False
        }
    )
    assert response.status_code == 422  # Unprocessable Entity

    # Invalid data types (e.g., price as string)
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "description": "Price as string",
            "price": "not-a-float",
            "category": "Invalid Category",
            "stock": 10,
            "featured": False
        }
    )
    assert response.status_code == 422

def test_update_product_invalid_data(client, db):
    # Create a product to update
    response = client.post(
        "/products/",
        json={
            "name": "Another Updatable Product",
            "description": "Original Description",
            "price": 89.99,
            "category": "Original Category",
            "stock": 20,
            "featured": True
        }
    )
    assert response.status_code == 200
    product = response.json()["product"]

    # Attempt to update with invalid data types
    response = client.put(
        f"/products/{product['id']}",
        json={
            "price": "invalid-price"  # Should be a float
        }
    )
    assert response.status_code == 422

def test_get_products_pagination(client, db):
    # Create multiple products
    for i in range(1, 6):
        client.post(
            "/products/",
            json={
                "name": f"Paginated Product {i}",
                "description": f"Description {i}",
                "price": 10.0 * i,
                "category": "Pagination Category",
                "stock": 10 * i,
                "featured": i % 2 == 0
            }
        )
    
    # Fetch first 2 products
    response = client.get("/products/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Fetch next 2 products
    response = client.get("/products/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Fetch remaining products
    response = client.get("/products/?skip=4&limit=10")
    assert response.status_code == 200
    data = response.json()
    # Adjust based on how many products were initially present
    assert len(data) >= 1

def test_featured_products(client, db):
    # Create featured and non-featured products
    client.post(
        "/products/",
        json={
            "name": "Featured Product",
            "description": "This is featured",
            "price": 99.99,
            "category": "Featured Category",
            "stock": 50,
            "featured": True
        }
    )
    client.post(
        "/products/",
        json={
            "name": "Non-Featured Product",
            "description": "This is not featured",
            "price": 49.99,
            "category": "Non-Featured Category",
            "stock": 30,
            "featured": False
        }
    )

    # Fetch all products and verify featured status
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    for product in data:
        if product["name"] == "Featured Product":
            assert product["featured"] is True
        elif product["name"] == "Non-Featured Product":
            assert product["featured"] is False

def test_create_products_for_cart(client):
    products = [
        {
            "name": "Cart Test Product 1",
            "description": "First product for cart tests",
            "price": 10.0,
            "category": "Test Category",
            "stock": 50,
            "featured": False
        },
        {
            "name": "Cart Test Product 2",
            "description": "Second product for cart tests",
            "price": 20.0,
            "category": "Test Category",
            "stock": 30,
            "featured": True
        },
        {
            "name": "Cart Test Product 3",
            "description": "Third product for cart tests",
            "price": 15.0,
            "category": "Test Category",
            "stock": 20,
            "featured": False
        }
    ]
    for product_data in products:
        response = client.post(
            "/products/",
            json=product_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        product = data["product"]
        assert product["name"] == product_data["name"]