# services/__init__.py
from .user import (
    get_user,
    get_user_by_username,
    get_user_by_email,
    create_user,
    authenticate_user,
)
from .product import (
    get_product,
    get_product_by_name,
    get_products,
    create_product,
    update_product,
    delete_product,
)

__all__ = [
    "get_user",
    "get_user_by_username",
    "get_user_by_email",
    "create_user",
    "authenticate_user",
    "get_product",
    "get_product_by_name",
    "get_products",
    "create_product",
    "update_product",
    "delete_product",
]
