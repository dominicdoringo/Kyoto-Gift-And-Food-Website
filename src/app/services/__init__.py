# services/__init__.py

from app.services.user import (
    get_user,
    get_user_by_email,
    get_all_users,
    create_user,
    authenticate_user,
    update_user,
    delete_user,
    change_user_password,
    deactivate_user,
    verify_user_email,
    save_profile_picture,
)
from app.services.cart import (
    get_cart_items,
    add_cart_item,
    update_cart_item,
    remove_cart_item,
    clear_cart,
)
