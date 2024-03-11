import pytest
from fastapi.testclient import TestClient

# from httpx import AsyncClient


def test_create_user(client: TestClient):
    body = {
            "user": {
            "userType": "seller",
            "userName": "string",
            "email": "user@example.com",
            "password": "string"
        },
        "accountDetails": {
            "name": "string",
            "image": "string"
        }
    }
    response = client.post(
        "/users/",
        json=body,
        headers={"Content-Type": "application/json"},

    )
    print(response.json())
    assert response.status_code == 201

def test_create_user_invalid(client: TestClient):
    body = {
        "user": {
            "userType": "seller",
            "userName": "string",
            "email": "email.@example.com",
            "password": "XXXXXX"

        },
        "accountDetails": {
            "name": "string",
            "image": "string"
        }

    }
    response = client.post(
        "/users/",
        json=body,
        headers={"Content-Type": "application/json"},
    )
    print(response.json())
    assert response.status_code == 422
    assert response.json()["message"][0]["msg"] == "value is not a valid email address: An email address cannot have a period immediately before the @-sign."

# @pytest.mark.anyio
# def test_list_users(client: AsyncClient):
#     response = client.get(
#         "/users/",
#         headers={"Content-Type": "application/json"},
#     )
#     assert response.status_code == 200
#     assert response.json() == []