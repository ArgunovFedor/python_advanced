from main import app
from fastapi.testclient import TestClient
client = TestClient(app)

def test_read_main():
    response = client.get("/recipe/")
    assert response.status_code == 200
