from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import account_details_collection, user_collection

from ..models.user import (
    UserCollectionModel,
    UserDeleteResponseModel,
)
from ..models.user_account_details import (
    UserAccountDetailsCreateRequestModel,
    UserAccountDetailsCreateResponseModel,
    UserAccountDetailsModel,
)

user_router = APIRouter()


@user_router.post(
    "/users/",
    response_description="Add new user",
    response_model=UserAccountDetailsCreateResponseModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(
    body: UserAccountDetailsCreateRequestModel,
) -> UserAccountDetailsCreateResponseModel:
    """
    Insert a new user record.

    A unique `id` will be created and provided in the response.
    """
    user = body.user

    now = int(datetime.utcnow().timestamp())
    user_data = user.model_dump()
    user_data.update({"createdAt": now, "updatedAt": now, "lastLoginAt": now})
    new_user = await user_collection.insert_one(user_data)

    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    accountDetails = body.accountDetails
    account_details = accountDetails.model_dump(by_alias=True)
    account_details["userID"] = new_user.inserted_id
    account_details.update({"createdAt": now, "updatedAt": now})

    new_account_details = await account_details_collection.insert_one(account_details)

    created_account_details = await account_details_collection.find_one(
        {"_id": new_account_details.inserted_id}
    )

    return UserAccountDetailsCreateResponseModel(
        user=created_user, accountDetails=created_account_details
    )


@user_router.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollectionModel,
    response_model_by_alias=False,
)
async def list_users():
    """
    List all of the user data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return UserCollectionModel(users=await user_collection.find().to_list(1000))


@user_router.get(
    "/users/{id}",
    response_description="Get user by user ID",
    response_model=UserAccountDetailsModel,
    response_model_by_alias=False,
)
async def show_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (user := await user_collection.find_one({"_id": ObjectId(id)})) is not None:
        accountDetails = await account_details_collection.find_one(
            {"userID": ObjectId(id)}
        )
        return UserAccountDetailsModel(user=user, accountDetails=accountDetails)
    raise HTTPException(status_code=404, detail="User not found")


@user_router.delete(
    "/users/{id}",
    response_description="Delete user by user ID",
    response_model=UserDeleteResponseModel,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def delete_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (await user_collection.find_one({"_id": ObjectId(id)})) is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user_collection.delete_one({"_id": ObjectId(id)})
    await account_details_collection.delete_one({"userID": ObjectId(id)})
    return UserDeleteResponseModel(message="User deleted successfully")
