# models/admin.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import User
from app.core.database import Base


class Admin(User):
    __tablename__ = "admins"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Admin-specific relationships or fields can be added here

    # Inheritance configuration
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
