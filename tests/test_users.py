import pytest


def user_payload(
    name="Paul",
    email="paul@atu.ie",
    age=25,
    student_id="S1234567",
):
    return {
        "name": name,
        "email": email,
        "age": age,
        "student_id": student_id,
    }


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Paul"
    assert data["email"] == "paul@atu.ie"


@pytest.mark.parametrize("bad_student_id", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post("/api/users", json=user_payload(student_id=bad_student_id))
    assert response.status_code == 422


def test_duplicate_user_returns_409(client):
    client.post("/api/users", json=user_payload())

    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()


def test_get_users_returns_created_users(client):
    created = client.post(
        "/api/users", json=user_payload(name="Alice", email="alice@atu.ie")
    ).json()

    response = client.get("/api/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == created["id"]
    assert data[0]["name"] == "Alice"


def test_get_existing_user_returns_200(client):
    user_id = client.post("/api/users", json=user_payload()).json()["id"]

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_user(client):
    user_id = client.post("/api/users", json=user_payload()).json()["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404


def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")

    assert response.status_code == 404