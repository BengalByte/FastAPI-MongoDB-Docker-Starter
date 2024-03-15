from pydantic import field_validator, EmailStr, BaseModel

from app.core.mixins import get_password_hash, verify_password_hash


class UserCreateDto(BaseModel):
    userName: str
    email: EmailStr
    password: str

