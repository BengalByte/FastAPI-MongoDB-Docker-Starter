import os

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
db = client.worktite
user_collection = db.get_collection("users")
account_details_collection = db.get_collection("accountDetails")
