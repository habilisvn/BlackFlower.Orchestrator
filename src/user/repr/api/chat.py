from fastapi import APIRouter, Depends
from pydantic import BaseModel

from user.repr.dependencies import get_current_user


router = APIRouter(
    prefix="/v1/chat",
    tags=["chat"],
    dependencies=[Depends(get_current_user)],
)


class ChatMessage(BaseModel):
    message: str


@router.post("")
async def chat(message: ChatMessage):
    return {"reply": "Received message!"}
