from enum import Enum
from typing import Optional

from pydantic import ConfigDict, EmailStr, Field

from app.core.mixins import TimeStampMixin, PyObjectId


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class AccountDetailsBaseModel(TimeStampMixin):
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
    billingEmail: EmailStr | None = Field(None)
    mailingAddress: str | None = Field(None)
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
            "billingEmail": "johndoe@email.com",
            "mailingAddress": "123, Example Street, Example City, Example Country",
            "createdAt": "2021-07-01",
            "updatedAt": "2021-07-01",
        },
    )


class AccountDetailsModel(AccountDetailsBaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)


class AccountDetailsCreateRequestModel(AccountDetailsBaseModel):
    pass


class AccountDetailsCreateResponseModel(AccountDetailsBaseModel):
    pass


class AccountDetailsUpdateRequestModel(AccountDetailsModel):
    pass


class AccountDetailsUpdateResponseModel(AccountDetailsModel): ...
