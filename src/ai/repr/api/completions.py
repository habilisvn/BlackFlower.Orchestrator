from fastapi import APIRouter

from ai.domain.entities import ChatMessage
from ai.repr.validations import ChatInput, ChatOutput
from common.dependencies.huggingface import ChatServiceDpd


router = APIRouter(
    prefix="/v1/chat/completions",
    tags=["chat"],
    # dependencies=[Depends(get_current_user)],
)


@router.post("")
async def chat(input: ChatInput, chat_service: ChatServiceDpd) -> ChatOutput:
    chat_msg = ChatMessage(role="user", content=input.message)
    reply = await chat_service.send_message(chat_msg)

    return ChatOutput(reply=reply)
