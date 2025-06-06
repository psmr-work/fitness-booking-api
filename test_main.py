from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_classes_default_timezone():
    response = client.get("/classes")
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    assert "name" in response.json()[0]
    assert "datetime" in response.json()[0]

def test_get_classes_custom_timezone():
    response = client.get("/classes?tz=UTC")
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    assert "datetime" in response.json()[0]

def test_get_classes_invalid_timezone():
    response = client.get("/classes?tz=Invalid/Zone")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid timezone"

def test_post_booking_success():
    response = client.post("/book", json={
        "class_id" : 1,
        "client_name": "Test User1",
        "client_email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["client_name"] == "Test User1"
    assert response.json()["client_email"] == "test@example.com"

def test_post_booing_failure_no_slots():
    for _ in range(10): #booking until full
        client.post("/book", json={
            "class_id":2,
            "client_name": f"User{_}",
            "client_email" : f"user{_}@example.com"
        })
    response = client.post("/book", json={
        "class_id":2,
        "client_name": "Extra",
        "client_email" : "extra@example.com"
    }) 
    assert response.status_code == 400
    assert "No slots available" in response.json()["detail"]


def test_get_bookings_for_email():
    response = client.get("/bookings", params={"client_email":"test@example.com"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["client_email"] == "test@example.com"


