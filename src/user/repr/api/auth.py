from typing import Annotated
from fastapi import Depends, APIRouter, Response
from datetime import timedelta

from common.dependencies import SettingsDependency
from user.domain.entities import UserEntity
from user.repr.dependencies import validate_user_exists
from user.utils import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def get_access_token(
    response: Response,
    settings: SettingsDependency,
    user: Annotated[UserEntity, Depends(validate_user_exists)]
) -> dict[str, str]:
    access_token_expires = timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    # Set HTTPOnly cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,  # Only send cookie over HTTPS (if True)
        samesite="none",  # Temporarily disabled CSRF protection
        # Convert minutes to seconds
        max_age=settings.jwt_access_token_expire_minutes * 60,
        path="/"  # Cookie available for all paths
    )

    return {"message": "Successfully logged in"}
