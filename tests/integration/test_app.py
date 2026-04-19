from fastapi.testclient import TestClient

from ai_multicloud_agent.main import app


def test_integration_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["environment"] == "development"
