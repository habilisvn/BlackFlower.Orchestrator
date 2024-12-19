from fastapi import APIRouter

from chat.repr.api.chat import router as chat_router

router = APIRouter(
    prefix="/api",
)
router.include_router(chat_router)
