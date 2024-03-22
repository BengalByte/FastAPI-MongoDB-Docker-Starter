from pydantic import BaseModel


class Token(BaseModel):
    refresh_token: str
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str
