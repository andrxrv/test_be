import os

import httpx
import pytest

BASE_URL = os.getenv("BOOKER_BASE_URL", "https://restful-booker.herokuapp.com")
USERNAME = os.getenv("BOOKER_USERNAME", "admin")
PASSWORD = os.getenv("BOOKER_PASSWORD", "password123")


def login(client: httpx.Client, username: str, password: str) -> httpx.Response:
    """POST /auth. Note: the API answers 200 even for bad credentials."""
    return client.post("/auth", json={"username": username, "password": password})


def create_booking(client: httpx.Client, payload: dict) -> httpx.Response:
    """POST /booking. No auth required."""
    return client.post("/booking", json=payload)


@pytest.fixture(scope="session")
def api_client():
    """Unauthenticated client shared by the whole test session."""
    with httpx.Client(
        base_url=BASE_URL,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        timeout=30,
    ) as client:
        yield client


@pytest.fixture(scope="session")
def auth_token(api_client):
    """Logs in once per session and returns the token."""
    response = login(api_client, USERNAME, PASSWORD)
    assert response.status_code == 200, f"Login failed: {response.status_code} {response.text}"

    token = response.json().get("token")
    assert token, f"No token in auth response: {response.text}"
    return token


@pytest.fixture(scope="session")
def auth_client(auth_token):
    """Client that sends the token as a cookie, for PUT/PATCH/DELETE /booking."""
    with httpx.Client(
        base_url=BASE_URL,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        cookies={"token": auth_token},
        timeout=30,
    ) as client:
        yield client


@pytest.fixture
def booking_payload():
    """Default valid body for POST /booking. Tests can change it before using it."""
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def booking_id(api_client, auth_client, booking_payload):
    """Creates a booking, yields its id and deletes it after the test."""
    response = create_booking(api_client, booking_payload)
    assert response.status_code == 200, f"Create booking failed: {response.status_code} {response.text}"

    booking_id = response.json()["bookingid"]
    yield booking_id

    # Cleanup; ignore the result in case the test already deleted it
    auth_client.delete(f"/booking/{booking_id}")
