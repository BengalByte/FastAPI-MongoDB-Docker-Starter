from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator, field_validator

from app.core.mixins import TimeStampMixin, verify_password_hash, get_password_hash

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserType(int, Enum):
    ADMIN = 1
    SELLER = 2
    SUPER_ADMIN = 0


class CommonModel(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")


class UserBaseSchema(CommonModel, TimeStampMixin):
    userType: UserType = Field(default=UserType.SELLER)
    userName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    lastLoginAt: datetime = datetime.now()
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "userType": "seller",
            "userName": "John Doe",
            "email": "john@email.com",
            "password": "XXXXXXXX",
        },
    )

    def verify_password(self, password: str) -> bool:
        return verify_password_hash(password, self.password)

    def make_hash(self):
        if not self.password:
            raise ValueError("password is required")
        self.password = get_password_hash(self.password)
        return self



class UserModel(UserBaseSchema):
    id: PyObjectId = Field(alias="_id")
    createdAt: int = Field(...)
    updatedAt: int = Field(...)
    lastLoginAt: int = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "createdAt": "2021-07-01",
            "updatedAt": "2021-07-01",
            "lastLoginAt": "2021-07-01",
        },
    )


class UserCreateRequestModel(UserBaseSchema): ...


class UserCreateResponseModel(UserModel): ...


class UserUpdateRequestModel(UserBaseSchema):
    id: PyObjectId = Field(alias="_id")


class UserUpdateResponseModel(UserBaseSchema): ...


class UserDeleteResponseModel(BaseModel):
    message: str = Field(...)


class UserGetResponseModel(UserModel): ...


class UserCollectionModel(BaseModel):
    """
    A container holding a list of `UserModel` instances.
    """

    users: List[UserModel]
