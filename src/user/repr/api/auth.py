from typing import Annotated, Any
from fastapi import Depends, APIRouter, Response
from datetime import timedelta

from common.dependencies.settings import SettingsDpd
from user.domain.entities import UserEntity
from user.repr.dependencies import validate_user_exists
from user.utils import create_access_token


router = APIRouter()
router_v1 = APIRouter(prefix="/v1/auth", tags=["auth"])
router_v2 = APIRouter(prefix="/v2/auth", tags=["auth"])


@router_v2.post("/login")
async def get_access_token_v1(
    settings: SettingsDpd,
    user: Annotated[UserEntity, Depends(validate_user_exists)],
) -> dict[str, str]:
    access_token_expires = timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router_v1.post("/login")
async def get_access_token_v2(
    response: Response,
    settings: SettingsDpd,
    user: Annotated[UserEntity, Depends(validate_user_exists)],
) -> dict[str, Any]:
    access_token_expires = timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    # Set HTTPOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Only send cookie over HTTPS (if True)
        samesite="none",  # Temporarily disabled CSRF protection
        # Convert minutes to seconds
        max_age=settings.jwt_access_token_expire_minutes * 60,
        path="/",  # Cookie available for all paths
    )

    return {"user_id": user.id}


router.include_router(router_v1)
router.include_router(router_v2)
