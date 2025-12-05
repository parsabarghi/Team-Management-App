from fastapi import Depends
from repositories.user_repository import UserRepository
from .repositories import get_user_repository
from services.user_service import UserService


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    """Dependency to get user services"""
    return UserService(user_repository)