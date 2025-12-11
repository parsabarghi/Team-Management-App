# from fastapi import Depends
# from sqlalchemy.orm import Session
# from db.session import get_db
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from .base_repository import BaseRepository
from models.users import User
from schemas.users_scheme import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()
    
    async def create_user_with_hashed_password(
        self, 
        user_in: UserCreate, 
        hashed_password: str
    ) -> User:
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hashed_password, 
            is_active=getattr(user_in, 'is_active', True),
            is_superuser=getattr(user_in, 'is_superuser', False)
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    # async def update_last_login(self, user_id:int):
    #     """Update user's last login timestamp"""
    #     query = (
    #         update(User)
    #         .where(User.id == user_id)
    #         .values(last_login=datetime.now(timezone.utc))
    #     )
    #     await self.db.execute(query)
    #     await self.db.commit()
    
    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        """Update user with optional password hashing"""
        update_data = user_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = User.hash_password(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get only active users"""
        result = await self.db.execute(
            select(User)
            .where(User.is_active)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def count_users(self) -> int:
        """Count total users"""
        result = await self.db.execute(select(func.count()).select_from(User))
        return result.scalar_one()
    
    async def count_active_users(self) -> int:
        """Count active users"""
        result = await self.db.execute(
            select(func.count()).select_from(User).where(User.is_active)
        )
        return result.scalar_one()