from sqlmodel import SQLModel, create_engine
from app.core.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Create the SQLite engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Required for SQLite
)


def init_db():
    from app import models  # Import models to register them with SQLModel
    SQLModel.metadata.create_all(bind=engine)
