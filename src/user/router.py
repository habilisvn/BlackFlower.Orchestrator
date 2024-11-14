from fastapi import APIRouter

from user.repr.api.auth import router as auth_router
from user.repr.api.user import router as user_router


router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)
router.include_router(auth_router)
router.include_router(user_router)
