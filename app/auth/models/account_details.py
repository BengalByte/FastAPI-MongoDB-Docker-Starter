from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class AccountDetailsBaseModel(BaseModel):
    userID: Optional[PyObjectId] = Field(default=None)
    name: str | None = Field(None)
    image: str | None = Field(None)
    gender: Gender | None = Field(None)
    email: EmailStr | None = Field(None)
    contactNumber: str | None = Field(None)
    companyNumber: str | None = Field(None)
    companyName: str | None = Field(None)
    vatNumber: str | None = Field(None)
    contactName: str | None = Field(None)
    billlingEmail: EmailStr | None = Field(None)
    maillingAddress: str | None = Field(None)
    createdAt: int | None = Field(None)
    updatedAt: int | None = Field(None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "name": "John Doe",
            "image": "https://www.example.com/image.jpg",
            "gender": "male",
            "email": "johndoe@email.com",
            "contactNumber": "1234567890",
            "companyNumber": "1234567890",
            "companyName": "John Doe Company",
            "vatNumber": "1234567890",
            "contactName": "John Doe",
            "billlingEmail": "johndoe@email.com",
            "maillingAddress": "123, Example Street, Example City, Example Country",
            "createdAt": "2021-07-01",
            "updatedAt": "2021-07-01",
        },
    )



class AccountDetailsModel(AccountDetailsBaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)


class AccountDetailsCreateRequestModel(AccountDetailsBaseModel): ...


class AccountDetailsCreateResponseModel(AccountDetailsBaseModel): ...


class AccountDetailsUpdateRequestModel(AccountDetailsModel): ...


class AccountDetailsUpdateResponseModel(AccountDetailsModel): ...
