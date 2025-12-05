from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from repositories.user_repository import UserRepository


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Dependency to get user repository"""
    return UserRepository(db)
