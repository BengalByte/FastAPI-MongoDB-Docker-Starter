from datetime import datetime
from enum import Enum
from typing import Annotated

from beanie import Document, Indexed
from pydantic import EmailStr, Field
from pydantic.functional_validators import BeforeValidator

from app.auth.models import MongoTables
from app.core.mixins import TimeStampMixin, verify_password_hash, get_password_hash, datetime_now_sec

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserType(int, Enum):
    ADMIN = 1
    SELLER = 2
    SUPER_ADMIN = 0


class UserBaseSchema(Document, TimeStampMixin):
    userType: UserType = Field(default=UserType.SELLER)
    userName: str = Field(...)
    email: EmailStr = Indexed(unique=True)
    lastLoginAt: datetime = Field(default_factory=datetime_now_sec)
    password: str = Field(...)

    class Settings:
        name = MongoTables.USER

    def verify_password(self, password: str) -> bool:
        return verify_password_hash(password, self.password)

    def make_hash(self):
        if not self.password:
            raise ValueError("password is required")
        self.password = get_password_hash(self.password)
        return self
