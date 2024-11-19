from pydantic import BaseModel


class AccessToken(BaseModel):
    pass


class AuthenticationService:
    async def get_access_token(self) -> AccessToken:
        pass
