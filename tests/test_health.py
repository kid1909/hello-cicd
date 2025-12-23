from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_add_returns_sum():
    r = client.get("/add?a=2&b=3")
    assert r.status_code == 200
    assert r.json() == {"result": 5}

def test_item_valid_id_returns_item():
    r = client.get("/items/10")
    assert r.status_code == 200
    data = r.json()
    assert data["item_id"] == 10
    assert data["name"] == "Item-10"

def test_item_invalid_id_returns_400():
    r = client.get("/items/-1")
    assert r.status_code == 400
    assert r.json()["detail"] == "item_id must be > 0"
