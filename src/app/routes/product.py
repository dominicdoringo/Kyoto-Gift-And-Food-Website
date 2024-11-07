# routes/product.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.services.product as product_service
from app.dependencies import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    Product,
)

router = APIRouter()


@router.get("/", response_model=list[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_service.get_products(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = product_service.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    new_product = product_service.create_product(db=db, product=product)
    return {"success": True, "product": new_product}


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = product_service.update_product(db=db, product_id=product_id, product=product)
    return {"success": True, "product": updated_product}


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = product_service.delete_product(db=db, product_id=product_id)
    return result
