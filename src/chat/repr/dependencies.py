from typing import Annotated
from fastapi import Depends


async def get_current_user(
    user_session: Annotated[UserSession, Depends(get_user_session)]
) -> UserSession:
    user = None

    return user
