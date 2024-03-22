import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt

from app.auth.dto.user import UserPayload

load_dotenv()


def _create_token(data: dict, expires_delta: int | None = None):
    user = UserPayload(**data).model_dump()
    to_encode = user.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(expires_delta))
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def create_access_token(data: dict):
    return _create_token(data, os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_refresh_token(data: dict):
    return _create_token(data, os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))


def decode_jwt(token) -> UserPayload:
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
            options={"verify_aud": False},
        )
        return UserPayload(**payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid token")
