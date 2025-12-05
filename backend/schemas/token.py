from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int

class TokenPayload(BaseModel):
    """Token payload schema for JWT decoding"""
    sub: str  # subject (usually user ID)
    exp: int  # expiration time
    type: str = "access"  # "access" or "refresh"
    scopes: list[str] = []

class TokenData(BaseModel):
    """Token data for internal use"""
    user_id: str
    email: str
    scopes: list[str] = []