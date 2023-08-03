"""
  Unit tests for fetch education fields API
"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.education_fields import router
from testing.test_config import API_URL
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")

client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learner-profile/education-fields"

def test_get_education_fields():
  url = api_url
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, "Status 200"
