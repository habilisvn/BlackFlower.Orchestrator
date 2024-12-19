from fastapi import APIRouter, UploadFile
import httpx

from chat.domain.entities import ChatMessage
from chat.repr.validations import ChatInput, ChatOutput
from common.dependencies.huggingface import ChatServiceDpd
from common.dependencies.settings import SettingsDpd


router = APIRouter(
    prefix="/v1/chat",
    tags=["chat"],
    # dependencies=[Depends(get_current_user)],
)


@router.post("/completions")
async def chat(input: ChatInput, chat_service: ChatServiceDpd) -> ChatOutput:
    chat_msg = ChatMessage(role="user", content=input.message)
    reply = await chat_service.send_message(chat_msg)

    return ChatOutput(reply=reply)


@router.post("/transcribe")
async def transcribe(
    upload_file: UploadFile, settings: SettingsDpd
) -> ChatOutput:
    # Get file data from upload_file
    file_data = upload_file.file.read()

    headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.huggingface_transcribe_url,
            headers=headers,
            data=file_data,
        )
        response_text = response.json()["text"]

    return ChatOutput(reply=response_text)
