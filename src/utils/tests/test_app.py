from fastapi.testclient import TestClient
from ...main import app

client = TestClient(app)


# Testing root endpoint response
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"details": "API Online"}
