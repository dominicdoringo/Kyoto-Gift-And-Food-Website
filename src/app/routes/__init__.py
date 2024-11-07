# routes/__init__.py
from fastapi import APIRouter

from app.routes import category, user, product, cart

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(product.router, prefix="/products", tags=["Products"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
