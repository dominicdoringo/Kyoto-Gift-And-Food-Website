# services/__init__.py
from .user import (
    get_user,
    get_user_by_username,
    get_user_by_email,
    create_user,
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
from .order import (
    create_order,
    get_order,
    get_orders,
    update_order,
    delete_order,
    get_order_status_history,
)
from .reward import (
    create_reward,
    get_reward,
    update_reward_points,
    cancel_reward_membership,
    redeem_reward_points,
)
from .auth import authenticate_user, login_user

__all__ = [
    # User services
    "get_user",
    "get_user_by_username",
    "get_user_by_email",
    "create_user",
    # Product services
    "get_product",
    "get_product_by_name",
    "get_products",
    "create_product",
    "update_product",
    "delete_product",
    # Cart services
    "get_cart_items",
    "add_cart_item",
    "update_cart_item",
    "remove_cart_item",
    "clear_cart",
    "get_cart_total",
    # Order services
    "create_order",
    "get_order",
    "get_orders",
    "update_order",
    "delete_order",
    "get_order_status_history",
    # Reward services
    "create_reward",
    "get_reward",
    "update_reward_points",
    "cancel_reward_membership",
    "redeem_reward_points",
    # Auth services
    "authenticate_user",
    "login_user",
]
