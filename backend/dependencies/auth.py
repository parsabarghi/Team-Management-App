from fastapi import Depends
from services.security_service import oauth2_scheme, SecurityService
# from repositories import UserRepository
from .repositories import get_user_repository, UserRepository
from models.users import User

async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> SecurityService:
    return SecurityService(user_repository)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: SecurityService = Depends(get_auth_service)
) -> User:
    return await auth_service.get_current_user(token)

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
    auth_service: SecurityService = Depends(get_auth_service)
) -> User:
    return await auth_service.get_current_active_user(current_user)

async def get_current_active_admin(
    current_user: User = Depends(get_current_active_user),
    auth_service: SecurityService = Depends(get_auth_service)
) -> User:
    return await auth_service.get_current_active_admin(current_user)

async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
    auth_service: SecurityService = Depends(get_auth_service)
) -> User:
    return await auth_service.get_current_superuser(current_user)