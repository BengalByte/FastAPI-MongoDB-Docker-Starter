from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.dto.token import Token, RefreshToken
from app.auth.dto.user import UserCreateDto, UserResponseDto
from app.auth.models.token import BlackListTokenSchema
from app.auth.models.user import UserBaseSchema
from app.auth.utils import create_access_token, create_refresh_token, decode_jwt

user_router = APIRouter()
auth_scheme = HTTPBearer()


@user_router.get(
    "/users/",
    response_description="List all users",
    response_model=List[UserResponseDto],
    response_model_by_alias=False,
)
async def list_users():
    return await UserBaseSchema.find_all().to_list(length=1)


@user_router.post(
    "/user",
    response_model=UserResponseDto,
    response_model_by_alias=False,
)
async def create_user(body: UserCreateDto):
    user = UserBaseSchema(**body.model_dump())
    try:
        user.make_hash()
        user = await user.insert()
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=str(e))


@user_router.post(
    "/login",
    response_model=Token,
    response_model_by_alias=False,
)
async def login_user(body: UserCreateDto):
    user = await UserBaseSchema.find_one({"email": body.email, "userName": body.userName})
    if user:
        if user.verify_password(body.password):
            access_token = create_access_token(data=user.model_dump())
            refresh_token = create_refresh_token(data=user.model_dump())
            return Token(access_token=access_token, refresh_token=refresh_token)
        else:
            return {"message": "Incorrect password"}
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@user_router.get(
    "/me",
    response_model_by_alias=False,
)
async def get_current_user(request: Request,
                           credentials: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]):
    return request.user


@user_router.post(
    "/rotate-token",
    response_model_by_alias=False,
)
async def get_current_user(body: RefreshToken):
    data = decode_jwt(body.refresh_token)
    b_token = BlackListTokenSchema(token=body.refresh_token)
    await b_token.insert()
    user = await UserBaseSchema.find_one({"email": data.email, "userName": data.userName})
    if user:
        access_token = create_access_token(data=user.model_dump())
        refresh_token = create_refresh_token(data=user.model_dump())
        return Token(access_token=access_token, refresh_token=refresh_token)
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@user_router.get("/token-blacklist")
async def get_current_user(body: RefreshToken):
    b_token = BlackListTokenSchema(token=body.refresh_token)
    return {"message": "ok"}
