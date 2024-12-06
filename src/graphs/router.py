from fastapi import APIRouter

from graphs.repr.api.node import router as node_router
from graphs.repr.api.relationship import router as relationship_router


router = APIRouter(
    prefix="/api",
)
router.include_router(node_router)
router.include_router(relationship_router)
