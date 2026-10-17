from fastapi.testclient import TestClient


def test_healthz(client: TestClient) -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_item(client: TestClient) -> None:
    response = client.post(
        "/items",
        json={"name": "widget", "description": "a small widget"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "widget"
    assert body["description"] == "a small widget"
    assert body["created_at"]


def test_list_items(client: TestClient) -> None:
    client.post("/items", json={"name": "first"})
    client.post("/items", json={"name": "second"})

    response = client.get("/items")

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["first", "second"]


def test_get_missing_item(client: TestClient) -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_rejects_blank_name(client: TestClient) -> None:
    response = client.post("/items", json={"name": ""})

    assert response.status_code == 422
