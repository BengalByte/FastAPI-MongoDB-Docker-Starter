import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


# import asyncio
# from typing import AsyncIterator

# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from httpx import AsyncClient


# @pytest.fixture(scope="session")
# def client():
#     from app.main import create_app
#     return TestClient(create_app())
  

# @pytest.fixture(scope="session")
# def event_loop():
#     return asyncio.get_event_loop()

# @pytest.fixture(scope="session")
# def anyio_backend():
#     return "asyncio"

# @pytest.fixture(scope="session")
# async def client():
#     from app.main import app
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         print("Client is ready")
#         yield client

# @pytest.fixture(scope="session")
# async def client():
#     from app.main import app
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         print("Client is ready")
#         yield ac
#         print("Client is done")
