from fastapi import APIRouter

from chat.repr.api.completions import router as chat_completions_router
from chat.repr.api.transcribe import router as chat_transcribe_router


router = APIRouter(
    prefix="/api",
)
router.include_router(chat_completions_router)
router.include_router(chat_transcribe_router)
