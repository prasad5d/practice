import pytest
import json
import os
import tempfile
from app.app import app as flask_app

@pytest.fixture(autouse=True)
def client():
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.close()
    os.unlink(tmp.name)  # file delete karo taaki empty start ho
    
    flask_app.config["TESTING"] = True
    flask_app.config["DATA_FILE"] = tmp.name
    
    with flask_app.test_client() as c:
        yield c
    
    if os.path.exists(tmp.name):
        os.remove(tmp.name)

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["status"] == "healthy"

def test_get_tasks_empty(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert json.loads(res.data) == []

def test_create_task(client):
    res = client.post("/api/tasks", json={"title": "Learn Docker"})
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data["title"] == "Learn Docker"
    assert data["done"] is False

def test_create_task_missing_title(client):
    res = client.post("/api/tasks", json={})
    assert res.status_code == 400

def test_update_task(client):
    res = client.post("/api/tasks", json={"title": "Learn CI/CD"})
    task_id = json.loads(res.data)["id"]
    res = client.put(f"/api/tasks/{task_id}", json={"done": True})
    assert res.status_code == 200
    assert json.loads(res.data)["done"] is True

def test_delete_task(client):
    res = client.post("/api/tasks", json={"title": "Learn Kubernetes"})
    task_id = json.loads(res.data)["id"]
    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code == 200
    tasks = json.loads(client.get("/api/tasks").data)
    assert len(tasks) == 0
