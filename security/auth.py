from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.db_models import Users_info
from sqlalchemy.orm import Session
from fastapi import Depends, Security, HTTPException
from database.db import get_db


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token valid for 30 minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT access token."""
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Returns the decoded token
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token and return user details."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload  # Returns decoded token (user data)