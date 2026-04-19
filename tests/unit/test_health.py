from ai_multicloud_agent.main import app


def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
