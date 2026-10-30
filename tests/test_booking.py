from conftest import create_booking


def test_create_booking(api_client, auth_client, booking_payload):
    response = create_booking(api_client, booking_payload)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["bookingid"], int)
    assert body["booking"] == booking_payload

    auth_client.delete(f"/booking/{body['bookingid']}")


def test_get_booking_by_id_matches_created_data(api_client, booking_id, booking_payload):
    response = api_client.get(f"/booking/{booking_id}")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    body = response.json()
    assert body["firstname"] == booking_payload["firstname"]
    assert body["lastname"] == booking_payload["lastname"]
    assert body["totalprice"] == booking_payload["totalprice"]
    assert body["depositpaid"] == booking_payload["depositpaid"]
    assert body["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"]
    assert body["bookingdates"]["checkout"] == booking_payload["bookingdates"]["checkout"]
    assert body["additionalneeds"] == booking_payload["additionalneeds"]
    # No unexpected extra fields
    assert body == booking_payload


def test_update_booking_checkout_date(api_client, auth_client, booking_id, booking_payload):
    # PUT replaces the whole booking, so send the full body with the new checkout
    updated_payload = {
        **booking_payload,
        "bookingdates": {**booking_payload["bookingdates"], "checkout": "2026-01-10"},
    }

    response = auth_client.put(f"/booking/{booking_id}", json=updated_payload)

    assert response.status_code == 200
    assert response.json()["bookingdates"]["checkout"] == "2026-01-10"
    assert response.json() == updated_payload

    # Confirm the change was saved
    saved = api_client.get(f"/booking/{booking_id}").json()
    assert saved["bookingdates"]["checkout"] == "2026-01-10"
    assert saved["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"]
    assert saved == updated_payload


def test_update_booking_without_token_is_forbidden(api_client, booking_id, booking_payload):
    response = api_client.put(f"/booking/{booking_id}", json=booking_payload)

    assert response.status_code == 403


def test_delete_booking(api_client, auth_client, booking_id):
    response = auth_client.delete(f"/booking/{booking_id}")

    # restful-booker answers 201 Created on a successful delete
    assert response.status_code == 201

    # Confirm the booking no longer exists
    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 404
