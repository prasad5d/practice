import pytest
import os
from app.app import app as flask_app

@pytest.fixture(autouse=True)
def client(tmp_path):
    tmp = str(tmp_path / "tasks.json")
    os.environ["DATA_FILE"] = tmp
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c
