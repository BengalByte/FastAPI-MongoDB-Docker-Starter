from pydantic import BaseModel

from ..models.account_details import (
    AccountDetailsCreateRequestModel,
    AccountDetailsCreateResponseModel,
    AccountDetailsModel,
    AccountDetailsUpdateRequestModel,
    AccountDetailsUpdateResponseModel,
)
from ..models.user import (
    UserCreateRequestModel,
    UserCreateResponseModel,
    UserModel,
    UserUpdateRequestModel,
    UserUpdateResponseModel,
)


class UserAccountDetailsCreateRequestModel(BaseModel):
    user: UserCreateRequestModel
    accountDetails: AccountDetailsCreateRequestModel


class UserAccountDetailsCreateResponseModel(BaseModel):
    user: UserCreateResponseModel
    accountDetails: AccountDetailsCreateResponseModel


class UserAccountDetailsModel(BaseModel):
    user: UserModel
    accountDetails: AccountDetailsModel


class UserAccountDetailsUpdateRequestModel(BaseModel):
    user: UserUpdateRequestModel
    accountDetails: AccountDetailsUpdateRequestModel


class UserAccountDetailsUpdateResponseModel(BaseModel):
    user: UserUpdateResponseModel
    accountDetails: AccountDetailsUpdateResponseModel
