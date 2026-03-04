import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET_KEY"] = "nyl3sDi8MozrL3z884XhTc8NHIwKnVjggIREvW4gn22"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token(client, username: str, password: str) -> str:
    r = client.post("/auth/token", data={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_auth_and_oficinas_flow(client):
    token = get_token(client, "admin", "ChangeMe_123!")
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/oficinas",
        json={"pais": "Colombia", "ciudad": "Bogota", "oficina": "Calle 1 #2-3"},
        headers=headers,
    )
    assert r.status_code == 201, r.text

    r = client.get("/oficinas?ciudad=Bogota", headers=headers)
    assert r.status_code == 200, r.text
    assert len(r.json()) >= 1