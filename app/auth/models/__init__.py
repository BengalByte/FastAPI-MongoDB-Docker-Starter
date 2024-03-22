from enum import Enum


class MongoTables(str, Enum):
    USER = 'users'
    USER_DETAILS = 'user_details'
    BLACK_LIST_TOKEN = 'black_list_token'
