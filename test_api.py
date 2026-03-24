import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def register_and_login(username="testuser", email="test@example.com", password="secret123"):
    client.post("/users/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/users/login", data={"username": username, "password": password})
    return resp.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# --- Health ---

def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# --- User Registration ---

def test_register_user():
    r = client.post("/users/register", json={
        "username": "alice", "email": "alice@example.com", "password": "pass1234"
    })
    assert r.status_code == 201
    assert r.json()["username"] == "alice"


def test_register_duplicate_email():
    client.post("/users/register", json={"username": "alice", "email": "alice@example.com", "password": "pass"})
    r = client.post("/users/register", json={"username": "bob", "email": "alice@example.com", "password": "pass"})
    assert r.status_code == 400


# --- Tasks CRUD ---

def test_create_task():
    token = register_and_login()
    r = client.post("/tasks/", json={"title": "Buy groceries", "priority": "high"}, headers=auth_headers(token))
    assert r.status_code == 201
    assert r.json()["title"] == "Buy groceries"


def test_list_tasks():
    token = register_and_login()
    h = auth_headers(token)
    client.post("/tasks/", json={"title": "Task 1"}, headers=h)
    client.post("/tasks/", json={"title": "Task 2"}, headers=h)
    r = client.get("/tasks/", headers=h)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_filter_tasks_by_priority():
    token = register_and_login()
    h = auth_headers(token)
    client.post("/tasks/", json={"title": "High task", "priority": "high"}, headers=h)
    client.post("/tasks/", json={"title": "Low task", "priority": "low"}, headers=h)
    r = client.get("/tasks/?priority=high", headers=h)
    assert all(t["priority"] == "high" for t in r.json())


def test_update_task():
    token = register_and_login()
    h = auth_headers(token)
    task_id = client.post("/tasks/", json={"title": "Old title"}, headers=h).json()["id"]
    r = client.patch(f"/tasks/{task_id}", json={"title": "New title", "completed": True}, headers=h)
    assert r.json()["completed"] is True
    assert r.json()["title"] == "New title"


def test_delete_task():
    token = register_and_login()
    h = auth_headers(token)
    task_id = client.post("/tasks/", json={"title": "To delete"}, headers=h).json()["id"]
    r = client.delete(f"/tasks/{task_id}", headers=h)
    assert r.status_code == 204
    r = client.get(f"/tasks/{task_id}", headers=h)
    assert r.status_code == 404


def test_unauthorized_access():
    r = client.get("/tasks/")
    assert r.status_code == 401
