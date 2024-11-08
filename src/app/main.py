# main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.openapi.utils import get_openapi
import logging
import time

from app.core.database import Base, engine
from app.routes import api_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Kyoto Gifts & Food API",
    description="This API powers the Kyoto Gifts & Food online store.",
    version="1.3.1",
    contact={
        "name": "Support",
        "email": "support@kyotostore.com",
    },
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production (e.g., ["https://yourdomain.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Logging Middleware
logger = logging.getLogger("uvicorn.access")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = request.headers.get("X-Request-ID", "N/A")
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"rid={idem} exception: {e}")
        raise e
    
    process_time = (time.time() - start_time) * 1000
    logger.info(f"rid={idem} completed_in={process_time:.2f}ms status_code={response.status_code}")
    return response

# Include API router
app.include_router(api_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Custom OpenAPI schema to include authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {},
                }
            },
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "responses" in method and "401" in method["responses"]:
                method.setdefault("security", []).append({"OAuth2PasswordBearer": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
