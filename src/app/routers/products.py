# app/routers/products.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=List[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=schemas.ProductCreateResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db, product)
    return {"success": True, "product": db_product}

@router.get("/{id}", response_model=schemas.Product)
def get_product(id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, id)
    return product

@router.put("/{id}", response_model=schemas.ProductUpdateResponse)
def update_product(id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    updated_product = crud.update_product(db, id, product_update)
    return {"success": True, "updatedProduct": updated_product}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, id)
    return

@router.get("/search", response_model=List[schemas.Product])
def search_products(query: str, db: Session = Depends(get_db)):
    products = crud.search_products(db, query)
    return products

@router.get("/category/{categoryName}", response_model=List[schemas.Product])
def get_products_by_category(categoryName: str, db: Session = Depends(get_db)):
    products = crud.get_products_by_category(db, categoryName)
    return products

@router.get("/filter", response_model=List[schemas.Product])
def filter_products(minPrice: float, maxPrice: float, db: Session = Depends(get_db)):
    products = crud.filter_products_by_price(db, minPrice, maxPrice)
    return products

@router.get("/featured", response_model=List[schemas.Product])
def get_featured_products(db: Session = Depends(get_db)):
    products = crud.get_featured_products(db)
    return products

@router.get("/{id}/inventory", response_model=schemas.ProductInventory)
def get_product_inventory(id: int, db: Session = Depends(get_db)):
    inventory = crud.get_product_inventory(db, id)
    return inventory

@router.put("/{id}/inventory", response_model=schemas.ProductInventoryUpdateResponse)
def update_product_inventory(id: int, inventory_update: schemas.ProductInventoryUpdate, db: Session = Depends(get_db)):
    response = crud.update_product_inventory(db, id, inventory_update.inventory)
    return response
