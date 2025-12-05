from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.users_scheme import UserBase, UserRegisteration
from models.users import Users
from db.session import get_db
from services.user_service import add_user

router = APIRouter()

@router.post("/register/user", response_model=UserBase, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_409_CONFLICT: {
        "description": "The User Already Exist"
    }
})
async def register(user: UserRegisteration, session: Session = Depends(get_db)) -> dict[str, UserBase]:
    clean_data = user.model_dump(exclude={"confirm_password"})
    try:
        user = await add_user(**clean_data, session=session)
    except HTTPException:
        raise
    response = UserBase(username=user.username, email=user.email)
    return response