from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.auth.routes.route_users import user_router


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
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": exc.errors()}
    )

def exception_handler():
    return {
        HTTPException: http_error_handler,
        RequestValidationError: validation_exception_handler
    }


def configure_routes(app):
    routers = [user_router]
    include_router(app, *routers)


def create_app():
    app = FastAPI(
        title="Student Course API",
        summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
    )
    configure_routes(app)
    add_middleware(app, [])
    add_exception_handler(app, exception_handler())

    return app


app = create_app()
if __name__ == "__main__":
    app = create_app()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)