# routes/products.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.products as product_service
from app.dependencies import get_db # DATA BASE ISSUE CONFUSED ABOUT 
from app.schemas.products import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.models.products import Product

router = APIRouter()

# Create a New Product (POST /api/products)
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = product_service.create_product(db=db, product=product)
    if not new_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    return new_product

# List All Products (GET /api/products)
@router.get("/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = product_service.get_all_products(db=db)
    return products

# Get Product Details by ID (GET /api/products/{id})
@router.get("/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db=db, product_id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update Product Information (PUT /api/products/{id})
@router.put("/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    updated_product = product_service.update_product(db=db, product_id=id, product_update=product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# Delete a Product (DELETE /api/products/{id})
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    success = product_service.delete_product(db=db, product_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return
