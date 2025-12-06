from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.users_scheme import UserBase, UserResponse, UserCreate, UserInDB
from models.users import User
from db.session import get_db
from services.user_service import UserService
from dependencies.services import get_user_service

router = APIRouter()

@router.post("/register/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_409_CONFLICT: {
        "description": "The User Already Exist"
    }
})
async def register(user_in: UserCreate, user_service: UserService = Depends(get_user_service)) -> dict[str, UserBase]:
   """ Creating New User => public endpoint """
   return user_service.create_user(user_in)