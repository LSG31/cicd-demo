from app.main import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "CI/CD demo application"


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_info_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    client = app.test_client()
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json["environment"] == "test"


def test_echo():
    client = app.test_client()
    response = client.post("/echo", json={"hello": "world"})
    assert response.status_code == 200
    assert response.json["echo"] == {"hello": "world"}
