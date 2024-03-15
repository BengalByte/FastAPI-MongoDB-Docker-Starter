import os
from enum import Enum

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


class DataBase:
    pass
    # def __init__(self, client):
    #     self.client = client
    #     self.db = client.college
    #     self.student_collection = self.db.get_collection("students")
    #     self.user_collection = self.db.get_collection("users")
    #     self.account_details_collection = self.db.get_collection("accountDetails")
    #     self.student_collection.create_index("roll_no")
    #     self.user_collection.create_index("email")
    #     self.account_details_collection.create_index("account_number")
    #     self.account_details_collection.create_index("ifsc")
    #     self.account_details_collection.create_index("branch")
    #     self.account_details_collection.create_index("name")
    #     self.account_details_collection.create_index("email")
    #     self.account_details_collection.create_index("phone_number")


USER = os.getenv("MONGOUSERNAME")
PASSWORD = os.getenv("MONGOPASSWORD")
MONGODB_URL = os.getenv("MONGODB_URL")

MONGODB_URL = (
    f"mongodb+srv://{USER}:{PASSWORD}@cluster0.fojn3vj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    if not MONGODB_URL
    else MONGODB_URL
)

client = AsyncIOMotorClient(MONGODB_URL)


class Tables(str, Enum):
    USER = 'users'
    USER_DETAILS = 'user_details'


async def setup_db():
    db = client[os.getenv("DB_NAME")]
    await db.pages.drop()
    return db


async def collections(ct: Tables):
    db = await setup_db()
    return db.get_collection(ct.value)


class Collections:
    def __init__(self, ct: Tables):
        self.ct = ct.value

    async def __call__(self):
        db = await setup_db()
        return db.get_collection(self.ct)



