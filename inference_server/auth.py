import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import sqlite3
from database import get_db_connection

# Security configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """Hash a password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def create_user(email: str, password: str, name: str) -> Optional[dict]:
    """Create a new user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            password_hash = get_password_hash(password)
            
            cursor.execute(
                "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
                (email, password_hash, name)
            )
            user_id = cursor.lastrowid
            
            return {
                "id": user_id,
                "email": email,
                "name": name
            }
    except sqlite3.IntegrityError:
        return None  # User already exists


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate a user and return user data if valid"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, name, password_hash FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        
        if not user:
            return None
        
        if not verify_password(password, user['password_hash']):
            return None
        
        # Update last login
        cursor.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.utcnow(), user['id'])
        )
        
        return {
            "id": user['id'],
            "email": user['email'],
            "name": user['name']
        }


def get_user_by_email(email: str) -> Optional[dict]:
    """Get user by email"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, name, created_at FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        
        if user:
            return dict(user)
        return None
