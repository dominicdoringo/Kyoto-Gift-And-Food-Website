# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.routers import users, auth, products, reviews, cart, orders, rewards, admin
from app.core.database import init_db

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Kyoto Gifts & Food API",
    description=(
        "This API powers the Kyoto Gifts & Food online store, allowing users to browse products, manage their carts, "
        "place orders, join the rewards program, and leave reviews for products. "
        "Admins have full control over product management, orders, users, and reporting."
    ),
    version="1.3.1",
    terms_of_service="http://kyotostore.com/terms/",
    contact={"email": "support@kyotostore.com"},
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Add other allowed origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Update with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Rate Limiting using slowapi
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse("Too Many Requests", status_code=429)

# Include routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(rewards.router)
app.include_router(admin.router)

# Initialize the database on startup
@app.on_event("startup")
def on_startup():
    init_db()
