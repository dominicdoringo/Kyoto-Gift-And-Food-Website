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
from .cart import (
    get_cart_items,
    add_cart_item,
    update_cart_item,
    remove_cart_item,
    clear_cart,
    get_cart_total,
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
    "get_cart_items",
    "add_cart_item",
    "update_cart_item",
    "remove_cart_item",
    "clear_cart",
    "get_cart_total",
]
