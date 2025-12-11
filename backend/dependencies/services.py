from fastapi import Depends
from repositories.user_repository import UserRepository
from .repositories import get_user_repository
from services.user_service import UserService
from services.security_service import SecurityService
from dependencies.auth import get_auth_service


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository), security_service: SecurityService = Depends(get_auth_service) ) -> UserService:
    """Dependency to get user services"""
    return UserService(user_repository,security_service)