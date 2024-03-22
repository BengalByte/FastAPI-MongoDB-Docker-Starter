from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from app.auth.models.token import BlackListTokenSchema
from app.auth.models.user import UserBaseSchema
from app.auth.routes.user import user_router
from app.core.database.beanie_db import mongo_database
from app.core.middleware.auth import BearerTokenAuthBackend


def include_router(app, *routers):
    for router in routers:
        app.include_router(router)


def add_middleware(app, middleware):
    for md in middleware:
        app.add_middleware(md)


def add_exception_handler(app, exception_handler):
    for ex, handler in exception_handler.items():
        app.add_exception_handler(ex, handler)


def http_error_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": exc.errors()},
    )


def exception_handler():
    return {
        HTTPException: http_error_handler,
        RequestValidationError: validation_exception_handler,
    }


def configure_routes(app: FastAPI):
    routers = [user_router]
    include_router(app, *routers)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = mongo_database()
    await init_beanie(database=db, document_models=[UserBaseSchema, BlackListTokenSchema])
    yield


def create_app():
    app = FastAPI(
        title="FastAPI MongoDB Docker Starter",
        summary="A starter application open-source boilerplate for quick web app and API setup. It combines FastAPI, "
                "MongoDB, and Docker for an efficient development and deployment experience",
        lifespan=lifespan
    )
    configure_routes(app)

    app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())
    add_middleware(app, [])
    add_exception_handler(app, exception_handler())

    return app


app = create_app()
if __name__ == "__main__":
    app = create_app()
    import uvicorn

    uvicorn.run('app.main:app', host="0.0.0.0", port=8000, reload=True)
