from fastapi import APIRouter

from ai.repr.api.completions import router as ai_completions_router
from ai.repr.api.transcribe import router as ai_transcribe_router


router = APIRouter(
    prefix="/api",
)
router.include_router(ai_completions_router)
router.include_router(ai_transcribe_router)
