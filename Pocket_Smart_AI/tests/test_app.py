import os

os.environ[
    "DATABASE_URL"
] = "sqlite:///./test_pocketsmart.db"

os.environ[
    "SECRET_KEY"
] = "test-secret"

os.environ[
    "GEMINI_API_KEY"
] = ""


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()[
        "status"
    ] == "ok"


def test_register_login_and_home():

    email = (
        "test@example.com"
    )


    response = client.post(

        "/register",

        data={

            "name":
                "Test User",

            "email":
                email,

            "password":
                "password123"
        },

        follow_redirects=False
    )


    assert response.status_code == 303


    assert (
        "access_token"
        in response.cookies
    )


    response = client.get(
        "/dashboard"
    )


    assert response.status_code == 200


    response = client.post(

        "/generate-home",

        json={

            "budget":
                50000,

            "rooms":
                [
                    "Living Room"
                ],

            "style":
                "modern",

            "items":
                [
                    {
                        "category":
                            "light",

                        "quantity":
                            2
                    }
                ],

            "city":
                "Chennai"
        }
    )


    assert response.status_code == 200


    assert (
        response.json()[
            "planner"
        ]
        == "home"
    )


    assert (
        response.json()[
            "source"
        ]
        == "demo"
    )


def test_login_token():

    response = client.post(

        "/token",

        data={

            "email":
                "test@example.com",

            "password":
                "password123"
        }
    )


    assert response.status_code == 200


    assert (
        response.json()[
            "token_type"
        ]
        == "bearer"
    )