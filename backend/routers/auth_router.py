from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token  
from dependencies.auth import get_auth_service  
from services.security_service import SecurityService

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: SecurityService = Depends(get_auth_service)
):
    try:
        # Your service returns (access_token, refresh_token)
        access_token, refresh_token = await auth_service.login_user(
            email=form_data.username,  # OAuth2 form uses "username" field
            password=form_data.password
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 7
        }
    except HTTPException:
        # Re-raise auth exceptions from service
        raise
    except Exception as e:
        # Generic fallback for unexpected errors
        print("FULL ERROR:", repr(e))
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )