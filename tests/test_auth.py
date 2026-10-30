import pytest

from conftest import PASSWORD, USERNAME, login


def test_login_returns_token(auth_token):
    assert isinstance(auth_token, str)
    assert len(auth_token) > 0


@pytest.mark.parametrize(
    "username, password",
    [
        (USERNAME, "wrong-password"),
        ("wrong-user", PASSWORD),
        ("", ""),
    ],
    ids=["bad_password", "bad_username", "empty_credentials"],
)
def test_login_with_invalid_credentials(api_client, username, password):
    response = login(api_client, username, password)

    # The API returns 200 with a "reason" field instead of 401
    assert response.status_code == 200
    body = response.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"
