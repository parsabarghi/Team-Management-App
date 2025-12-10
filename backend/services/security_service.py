from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from models.users import User
from repositories.user_repository import UserRepository
from dependencies.repositories import get_user_repository
from dependencies.services import get_user_service
from typing import Annotated


# pwd_context = CryptContext(
#     schemes=["bcrypt"], deprecated="auto"
# )
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SecurityService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends(get_user_repository)]):
        self.user_repo = user_repo
        self.pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)       
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        