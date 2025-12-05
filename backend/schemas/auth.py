from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LoginRequest(BaseModel):
    """User login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    remember_me: bool = False

class RegisterRequest(BaseModel):
    """User registration request schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    """Token refresh request schema"""
    refresh_token: str

class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)

class OAuth2LoginRequest(BaseModel):
    """OAuth2 login request schema"""
    provider: str  # "google", "github", etc.
    code: str
    redirect_uri: str