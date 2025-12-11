from datetime import timedelta, timezone, datetime
import uuid
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
from jose import JWTError, jwt
from models.users import User
# from repositories.user_repository import UserRepository
from dependencies.repositories import get_user_repository, UserRepository
# from dependencies.services import get_user_service
from typing import Tuple
from schemas.token import TokenData
from config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class SecurityService:

    def __init__(self, user_repo: get_user_repository):
        self.user_repo = user_repo
        self.pwd_context = pwd_context
    
    def get_password_hash(self, password: str) -> str:
        """Hash password using bcrypt"""
        return self.pwd_context.hash(password)
    
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Hash passwordn cheking"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "type": "access",
            "jti": str(uuid.uuid4()),  
            "iss": settings.TOKEN_ISSUER  # Add to config
        })
        return jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS  # Must exist in config
        )
        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "jti": str(uuid.uuid4()),
            "iss": settings.TOKEN_ISSUER
        })
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    def decode_token(self, token: str) -> dict:
        # return jwt.decode(
        #     token,
        #     settings.SECRET_KEY,
        #     algorithms=[settings.ALGORITHM],
        #     issuer=settings.TOKEN_ISSUER  # Validate issuer
        # )
        try:
            print(f"Decoding token: {token}")  # Temporary debug
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                issuer=settings.TOKEN_ISSUER
            )
            print(f"Token decoded successfully: {payload}")  # Temporary debug
            return payload
        except JWTError as e:
            print(f"Token decoding failed: {str(e)}")  # This will show the exact error
            raise

    async def authenticate_user(self, email: str, password: str) -> User|None:
        """
        Authenticate user by email and password
        Returns User object if successful, None otherwise
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
        
    async def get_current_user(self, token: str) -> User: 
        """
        Get current user from token
        This is the core authentication dependency
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Decode token
            payload = self.decode_token(token)
            
            # Validate token type
            token_type = payload.get("type")
            if token_type != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Get user ID from token
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            
            # Get token data for validation
            token_data = TokenData(user_id=user_id)
            
        except JWTError:
            raise credentials_exception
        
        # Get user from database
        user = await self.user_repo.get_by_id(int(token_data.user_id))
        if user is None:
            raise credentials_exception
        
        return user
    
    async def get_current_active_user(
        self,
        current_user: User
    ) -> User:
        """
        Get current active user
        Checks if user is active
        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user
    
    async def get_current_active_admin(
        self,
        current_user: User 
    ) -> User:
        """
        Get current active admin user
        Checks if user has admin privileges
        """
        if current_user.roles != "admin" and current_user.roles != "superuser":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    
    async def get_current_superuser(
        self,
        current_user: User
    ) -> User:
        """
        Get current superuser
        Checks if user is superuser
        """
        if current_user.roles != "superuser":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Superuser privileges required"
            )
        return current_user
    
    # Login & Token Management
    async def login_user(
        self,
        email: str,
        password: str
    ) -> Tuple[str, str]:
        """
        Handle user login
        Returns (access_token, refresh_token)
        """
        user = await self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens
        access_token = self.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        refresh_token = self.create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        # Update last login timestamp
        # await self.user_repo.update_last_login(user.id)
        
        return access_token, refresh_token
    
    async def refresh_access_token(self, refresh_token: str) -> str:
        """
        Refresh access token using refresh token
        Returns new access token
        """
        try:
            # Decode refresh token
            payload = self.decode_token(refresh_token)
            
            # Validate token type
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type for refresh",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Get user ID
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Verify user exists
            user = await self.user_repository.get_by_id(int(user_id))
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Create new access token
            new_access_token = self.create_access_token(
                data={"sub": str(user.id)},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return new_access_token
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )