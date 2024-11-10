# src/app/main.py

from fastapi import FastAPI, Request
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes.user import router as user_router
from app.core.middleware import AdvancedMiddleware  # Correct import path

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Rate Limiting Middleware
app.add_middleware(
    AdvancedMiddleware,
    max_requests=100,       # Maximum 100 requests
    window_seconds=60       # Per 60 seconds
)

# Include API router
app.include_router(user_router)

# Existing Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = request.headers.get("X-Request-ID")
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"rid={idem} start request path={request.url.path}")
    response = await call_next(request)
    logger.info(
        f"rid={idem} completed_in={response.headers.get('X-Process-Time')} status_code={response.status_code}"
    )
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}
