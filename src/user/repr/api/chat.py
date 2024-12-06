from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
async def chat(message: ChatMessage):
    return {"reply": "Received message!"}
