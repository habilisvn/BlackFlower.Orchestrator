from fastapi import APIRouter

from user.repr.api.auth import router as auth_router
from user.repr.api.user import router as user_router
from user.repr.api.chat import router as chat_router

router = APIRouter(
    prefix="/api",
)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(chat_router)
