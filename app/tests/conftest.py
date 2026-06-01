import pytest
import tempfile
import os
from app.app import app as flask_app

@pytest.fixture
def client():
    tmp = tempfile.mktemp(suffix=".json")
    flask_app.config["TESTING"] = True
    flask_app.config["DATA_FILE"] = tmp
    os.environ["DATA_FILE"] = tmp
    with flask_app.test_client() as c:
        yield c
    if os.path.exists(tmp):
        os.remove(tmp)
