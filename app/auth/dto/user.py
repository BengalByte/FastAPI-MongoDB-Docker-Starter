from pydantic import EmailStr, BaseModel

from app.auth.models.user import UserBaseSchema
from app.core.mixins import create_model_dto


# don't touch

class UserPayload(BaseModel):
    id: str
    userType: int
    email: EmailStr
    userName: str


class AuthUser(UserPayload):
    is_authenticated: bool = True


class UserCreateDto(BaseModel):
    userName: str
    email: EmailStr
    password: str


UserResponseDto = create_model_dto("UserResponseDto", UserBaseSchema, exclude_fields=['password', 'revision_id'])
