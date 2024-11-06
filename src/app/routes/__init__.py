from fastapi import APIRouter

from app.routes import category, user, cart

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
