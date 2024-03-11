from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserType(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    SUPERADMIN = "superAdmin"


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    userType: UserType = Field(default=UserType.SELLER)
    userName: str = Field(...)
    email: EmailStr = Field(...)
    createdAt: str = Field(...)
    updatedAt: str = Field(...)
    lastLoginAt: str = Field(...)
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "userType": "seller",
            "userName": "John Doe",
            "email": "johndoe@gmail.com",
            "createdAt": "2021-07-01",
            "updatedAt": "2021-07-01",
            "lastLoginAt": "2021-07-01",
            "password": "password",
        },
    )


class UserCreateModel(BaseModel):
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
            "email": "user@email.com",
            "password": "XXXXXXXX",
        },
    )


class UserCreateResponseModel(BaseModel):
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
            "email": "user@email.com",
            "password": "XXXXXXXX",
        },
    )
    id: PyObjectId = Field(alias="_id")
    createdAt: str = Field(...)
    updatedAt: str = Field(...)
    lastLoginAt: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "userType": "seller",
            "userName": "John Doe",
            "email": "user@email.com",
            "password": "XXXXXXXX",
            "id": "XXXXXXXXXXXXXX",
            "createdAt": "2021-07-01",
            "updatedAt": "2021-07-01",
            "lastLoginAt": "2021-07-01",
        },
    )


class UserUpdateModel(BaseModel):
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
            "email": "user@email.com",
            "password": "XXXXXXXX",
        },
    )


class UserCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    users: List[UserModel]
