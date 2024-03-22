import os

from dotenv import load_dotenv
from motor import motor_asyncio, core
from odmantic import AIOEngine
from pymongo.driver_info import DriverInfo

load_dotenv()

DRIVER_INFO = DriverInfo(name="fastapi-mongodb", version='0.1')

USER = os.getenv("MONGOUSERNAME")
PASSWORD = os.getenv("MONGOPASSWORD")
MONGODB_URL = os.getenv("MONGODB_URL")
MONGO_DB = os.getenv("DB_NAME")


class _MongoClientSingleton:
    instance = None
    mongo_client: motor_asyncio.AsyncIOMotorClient | None
    engine: AIOEngine

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                MONGODB_URL, driver=DRIVER_INFO
            )
        return cls.instance


def mongo_database() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[MONGO_DB]

