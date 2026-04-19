import pytest
from fastapi.testclient import TestClient

from ai_multicloud_agent.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
