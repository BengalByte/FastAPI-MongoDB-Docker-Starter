from typing import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator

from ..models.account_details import AccountDetailResponseModel
from ..models.user import UserCreateResponseModel

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserAccountDetailsModel(BaseModel):
    user: UserCreateResponseModel
    accountDetails: AccountDetailResponseModel
