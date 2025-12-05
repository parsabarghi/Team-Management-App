from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List, Literal
from .base import BaseSchema
from .token import Token
from enum import Enum

class Role(str, Enum):
    """User role enum"""
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"

class Permission(str, Enum):
    """User permission enum"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class UserBase(BaseSchema):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    role: Role = Role.USER
    permissions: List[Permission] = []

class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=128)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    is_active: Optional[bool] = None
    role: Optional[Role] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if v and not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserInDB(UserBase):
    """User schema for database operations"""
    hashed_password: str
    last_login: Optional[datetime] = None

class UserResponse(UserBase):
    """User response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

class UserProfile(UserResponse):
    """User profile schema with additional info"""
    last_login: Optional[datetime] = None
    login_count: int = 0

class UserWithToken(UserResponse):
    """User schema with token for login response"""
    token: Token

class UserSearch(BaseModel):
    """User search schema"""
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[Role] = None
    page: int = 1
    page_size: int = 10
    order_by: str = "created_at"
    order: Literal["asc", "desc"] = "desc"