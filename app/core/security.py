# app/core/security.py

import os
from datetime import datetime, timedelta
from typing import Dict
from app.core.settings import settings
from jose import jwt
from passlib.context import CryptContext


# ---------------------------------------------------------
# Security configuration
# ---------------------------------------------------------



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not configured")


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ---------------------------------------------------------
# Password utilities
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------
# JWT utilities
# ---------------------------------------------------------

def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)