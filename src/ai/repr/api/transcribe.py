from fastapi import APIRouter, UploadFile
import httpx

from common.dependencies.settings import SettingsDpd
from ai.repr.validations import ChatOutput


router = APIRouter(
    prefix="/v1/chat/transcribe",
    tags=["chat"],
    # dependencies=[Depends(get_current_user)],
)


@router.post("")
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
