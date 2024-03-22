from beanie import Document
from pydantic import Field

from app.auth.models import MongoTables
from app.core.mixins import TimeStampMixin


class BlackListTokenSchema(Document, TimeStampMixin):
    token: str = Field()

    class Settings:
        name = MongoTables.BLACK_LIST_TOKEN
