from typing import Annotated
from fastapi import Depends, APIRouter
from datetime import timedelta

from common.dependencies import SettingsDependency
from user.domain.entities import UserEntity
from user.repr.dependencies import validate_user_exists
from user.utils import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def get_access_token(
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
    return {"access_token": access_token, "token_type": "bearer"}
