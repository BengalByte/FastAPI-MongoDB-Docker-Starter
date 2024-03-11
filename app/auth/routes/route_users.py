from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status

from app.database import account_details_collection, user_collection

from ..models.user import UserCollection
from ..models.user_account_details import UserAccountDetailsModel

user_router = APIRouter()

@user_router.post(
        "/users/",
        response_description="Add new user",
        response_model=UserAccountDetailsModel,
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False,
) 
async def create_user(body: UserAccountDetailsModel) ->UserAccountDetailsModel: 
    """
    Insert a new user record.

    A unique `id` will be created and provided in the response.
    """
    user = body.user
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    accountDetails = body.accountDetails
    account_details = accountDetails.model_dump(by_alias=True, exclude=["id"])
    account_details["userID"] = new_user.inserted_id

    new_account_details = await account_details_collection.insert_one(
        account_details
    )
    
    created_account_details = await account_details_collection.find_one(
        {"_id": new_account_details.inserted_id}
    )

    return UserAccountDetailsModel(
        user=created_user,
        accountDetails=created_account_details
    )

@user_router.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_users():
    """
    List all of the user data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return UserCollection(users=await user_collection.find().to_list(1000))

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
    if (
        user := await user_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        accountDetails = await account_details_collection.find_one({"userID": ObjectId(id)})
        return UserAccountDetailsModel(
            user=user,
            accountDetails=accountDetails
        )
    raise HTTPException(status_code=404, detail="User not found")