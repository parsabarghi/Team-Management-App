from typing import Annotated
# from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.users_scheme import UserBase, UserResponse, UserCreate, UserInDB, UserWithToken
from models.users import User
# from db.session import get_db
from services.user_service import UserService
from dependencies.services import get_user_service
from dependencies.auth import get_current_active_user, get_current_active_admin,get_current_superuser


router = APIRouter()

@router.post("/register/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_409_CONFLICT: {
        "description": "The User Already Exist"
    }
})
async def register(user_in: UserCreate, user_service: UserService = Depends(get_user_service)) -> dict[str, UserBase]:
   """ Creating New User => public endpoint """
   return await user_service.create_user(user_in)

# @router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
# async def current_user(user_service: UserService = Depends(get_user_service)):
#    """ Get the cuurent user from db"""
#    return await user_service.get_current_user()

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.get("/admin-only")
async def admin_endpoint(
    current_user: User = Depends(get_current_active_admin)
):
    return {"message": "Admin access granted"}

@router.get("/superuser-only")
async def superuser_endpoint(
    current_user: User = Depends(get_current_superuser)
):
    return {"message": "Superuser access granted"}  