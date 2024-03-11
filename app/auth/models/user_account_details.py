from typing import Annotated, List, Optional

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from pydantic.functional_validators import BeforeValidator

from ..models.account_details import AccountDetailCreateModel, AccountDetailsModel
from ..models.user import UserCreateModel, UserModel

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserAccountDetailsModel(BaseModel):
    user: UserCreateModel
    accountDetails: AccountDetailCreateModel