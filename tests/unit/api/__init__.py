from fastapi.testclient import TestClient

from mammon_api.api import app

client = TestClient(app=app)
