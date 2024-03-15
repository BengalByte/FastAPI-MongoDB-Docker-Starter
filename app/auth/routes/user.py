from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from motor.core import AgnosticCollection

from app.database import Collections, Tables
from ..dto.user import UserCreateDto
from ..models.user import (
    UserDeleteResponseModel,
    UserBaseSchema
)
from ..models.user_account_details import (
    UserAccountDetailsModel,
)

user_router = APIRouter()

# dependencies
user_collection = Collections(Tables.USER)
user_details_collection = Collections(Tables.USER_DETAILS)


@user_router.get(
    "/users/",
    response_description="List all users",
    response_model=List[UserBaseSchema],
    response_model_by_alias=False,
)
async def list_users(collection=Depends(user_collection)):
    return await collection.find().to_list(1000)


@user_router.post("/user")
async def create_user(body: UserCreateDto, collection: AgnosticCollection = Depends(user_collection)):
    user = UserBaseSchema(**body.model_dump())
    try:
        await collection.insert_one(user.make_hash().model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Done"}


@user_router.post("/login")
async def create_user(body: UserCreateDto, collection: AgnosticCollection = Depends(user_collection)):
    data = await collection.find_one(filter={"userName": body.userName, "email": body.email})
    if data:
        return {"data": UserBaseSchema(**data)}
    return {"message": "User not found"}


@user_router.get(
    "/users/{id}",
    response_description="Get user by user ID",
    response_model=UserAccountDetailsModel,
    response_model_by_alias=False,
)
async def show_user(id: str):
    pass


@user_router.delete(
    "/users/{id}",
    response_description="Delete user by user ID",
    response_model=UserDeleteResponseModel,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def delete_user(id: str):
    pass
