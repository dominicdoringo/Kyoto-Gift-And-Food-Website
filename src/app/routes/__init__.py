# routes/__init__.py
from fastapi import APIRouter
from .user import router as user_router
from .product import router as product_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
