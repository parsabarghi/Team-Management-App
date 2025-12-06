# from typing import Annotated
# from sqlalchemy import select
# from models.users import pwd_context
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
# from fastapi import Depends, HTTPException, status
# from db.session import get_db
# # from models.users import Users
# from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio

from typing import Optional
from fastapi import HTTPException, status
from ..repositories.user_repository import UserRepository
from ..schemas.users_scheme import UserCreate, UserResponse
from ..models.users import User

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user(self, user_in: UserCreate) -> UserResponse:
        """Business logic: Create user with validation"""
        # Check if email already exists
        existing_user = await self.user_repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_username = await self.user_repository.get_by_username(user_in.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create user (business logic orchestrates the repository call)
        user = await self.user_repository.create_user(user_in)
        return UserResponse.model_validate(user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID with business logic"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    
    async def get_current_user(self, current_user: User) -> UserResponse:
        """Get current user profile"""
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return UserResponse.model_validate(current_user)





# async def add_user(username: str, email:str, password:str, session: Session=Annotated[AsyncSession, Depends(get_db)]) -> Users | None:
#     # check duplicate before hashing to save cpu
#     if await session.scalar(select(Users).where(Users.username==username)):
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username Taken")
#     if await session.scalar(select(Users).where(Users.email == email)):
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email taken")
    
#     hashed_password = await asyncio.to_thread(pwd_context.hash, password)
#     db_user = Users(
#         username = username,
#         email=email,
#         hashed_password=hashed_password
#     )
#     session.add(db_user)
#     try:
#         await session.commit()
#         await session.refresh(db_user)
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
#     finally:
#         await session.close()
#         return db_user