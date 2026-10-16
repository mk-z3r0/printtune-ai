from fastapi.testclient import TestClient

from printtune.api import app


def test_health():
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    assert response.json()["mode"] == "read-only"
