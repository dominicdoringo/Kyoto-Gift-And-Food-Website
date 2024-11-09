#src/app/main.py
from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
# Configure CORS middleware

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    idem = request.headers.get("X-Request-ID")
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"rid={idem} start request path={request.url.path}")
    response = await call_next(request)
    logger.info(f"rid={idem} completed_in={response.headers.get('x-process-time')} status_code={response.status_code}")
    return response
@app.get("/")
def read_root():
    return {"Hello": "World"}
#end code