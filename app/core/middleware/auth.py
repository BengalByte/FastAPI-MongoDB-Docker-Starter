from typing import Optional

from fastapi import Request
from jose import JWTError
from starlette.authentication import AuthenticationBackend

from app.auth.dto.user import AuthUser
from app.auth.models.user import UserBaseSchema
from app.auth.utils import decode_jwt


class BearerTokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "authorization" not in request.headers:
            return

        auth = request.headers.get("authorization")
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            decoded = decode_jwt(token)
            email: str = decoded.email
        except (ValueError, UnicodeDecodeError, JWTError) as exc:
            return
        user = await get_user(email)
        user = AuthUser(**user.model_dump())
        return auth, user


async def get_user(email: Optional[str]) -> Optional[UserBaseSchema]:
    if email:
        return await UserBaseSchema.find_one({"email": email})
    else:
        return None


# Middleware function
async def bind_user_to_request(request: Request):
    token = request.headers.get("authorization", None)
    if not token:
        return
    user = await get_user(token)
    request.state.user = user
