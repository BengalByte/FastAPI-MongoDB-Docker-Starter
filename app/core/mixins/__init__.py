from datetime import datetime
from typing import Annotated, Optional

from passlib.context import CryptContext
from pydantic import BaseModel, create_model
from pydantic.functional_validators import BeforeValidator, model_validator

PyObjectId = Annotated[str, BeforeValidator(str)]


class AuthorMixin(BaseModel):
    owner_id: Optional[PyObjectId] = None


class TimeStampMixin(BaseModel):
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

    @model_validator(mode='after')
    def number_validator(self):
        self.updatedAt = datetime.now()
        return self


class AuthorWithTimeStamp(AuthorMixin, TimeStampMixin):
    pass


def create_model_dto(name, cls, *include_fields):
    fields = {}
    for field_name, field_type in cls.model_fields.items():
        if include_fields and field_name not in include_fields:
            continue
        fields[field_name] = (field_type.annotation, ...)
    dto = create_model(name, **fields)
    return dto


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
