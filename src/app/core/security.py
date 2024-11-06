# app/security.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# Secret key to encode the JWT tokens
SECRET_KEY = "your-secret-key"  # Replace with a secure random key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time in minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiry time
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
