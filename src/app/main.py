# src/app/main.py

from fastapi import FastAPI, Request
import logging

from app.core.database import Base, engine
from app.routes.user import router as user_router

Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(user_router)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}
