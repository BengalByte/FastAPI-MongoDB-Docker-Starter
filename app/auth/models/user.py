from enum import Enum
from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserType(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    SUPERADMIN = "superAdmin"


class UserBaseModel(BaseModel):
    userType: UserType = Field(default=UserType.SELLER)
    userName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
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


class UserModel(UserBaseModel):
    id: PyObjectId = Field(alias="_id")
    createdAt: str = Field(...)
    updatedAt: str = Field(...)
    lastLoginAt: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "createdAt": "2021-07-01",
            "updatedAt": "2021-07-01",
            "lastLoginAt": "2021-07-01",
        },
    )


class UserCreateRequestModel(UserBaseModel): ...


class UserCreateResponseModel(UserModel): ...


class UserUpdateRequestModel(UserBaseModel):
    id: PyObjectId = Field(alias="_id")


class UserUpdateResponseModel(UserModel): ...


class UserDeleteResponseModel(BaseModel):
    message: str = Field(...)


class UserGetResponseModel(UserModel): ...


class UserCollectionModel(BaseModel):
    """
    A container holding a list of `UserModel` instances.
    """

    users: List[UserModel]
