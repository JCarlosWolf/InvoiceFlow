# app/core/security.py

import os
from datetime import datetime, timedelta
from typing import Dict

from jose import jwt
from passlib.context import CryptContext


# ------------------------------------------------------------------
# Security configuration
# ------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ------------------------------------------------------------------
# Password utilities
# ------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------------
# JWT utilities
# ------------------------------------------------------------------

def create_access_token(data: Dict) -> str:
    """
    Create a signed JWT access token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)