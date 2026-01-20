from fastapi.testclient import TestClient
from app.main import app

def test_predict_returns_probabilities():
    with TestClient(app) as client:
        payload = {"features": [5.1, 3.5, 1.4, 0.2]}
        r = client.post("/predict", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "class_id" in data
        assert "probabilities" in data
        assert len(data["probabilities"]) == 3
        assert abs(sum(data["probabilities"]) - 1.0) < 1e-6

def test_predict_rejects_wrong_length():
    with TestClient(app) as client:
        r = client.post("/predict", json={"features": [1, 2, 3]})
        assert r.status_code == 400
