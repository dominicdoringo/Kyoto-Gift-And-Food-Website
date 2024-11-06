# app/main.py

from fastapi import FastAPI
from .routes import users, auth, products, reviews, cart, orders, rewards, admin

app = FastAPI(
    title="Kyoto Gifts & Food API",
    description="This API powers the Kyoto Gifts & Food online store.",
    version="1.3.1",
    terms_of_service="http://kyotostore.com/terms/",
    contact={
        "email": "support@kyotostore.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(rewards.router)
app.include_router(admin.router)
