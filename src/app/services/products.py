# services/product.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.products import Product
from app.schemas.products import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_all_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, product: ProductCreate):
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    product = get_product(db, product_id)
    if not product:
        return None

    if product_update.name is not None:
        product.name = product_update.name
    if product_update.description is not None:
        product.description = product_update.description
    if product_update.price is not None:
        product.price = product_update.price
    if product_update.stock is not None:
        product.stock = product_update.stock

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True
