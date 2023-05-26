"""
test file for progress.py
"""

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import os
from copy import deepcopy

from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.learner import router
from routes.progress import router as progress_router
from testing.test_config import API_URL
from schemas.schema_examples import (
  BASIC_LEARNER_EXAMPLE,
  BASIC_LEARNER_PROFILE_EXAMPLE,
  BASIC_LEARNING_RESOURCE_EXAMPLE,
)
from common.models import (Learner,LearnerProfile,LearningResource)

from common.utils.http_exceptions import add_exception_handlers

from common.testing.firestore_emulator import (
  firestore_emulator,
  clean_firestore
)

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")
app.include_router(progress_router, prefix="/learner-profile-service/api/v1")
client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learner"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_learner_progress_postive(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}

  if "Teamwork" not in learner_profile_dict["learning_goals"]:
    learner_profile_dict["learning_goals"].append("Teamwork")

  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.learner_id = learner.id
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  learning_resource_dict = deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  url = f"{api_url}/{learner.uuid}/progress"
  params = {"node_id": learning_resource.id,"node_type": "learning_resources"}
  resp = client_with_emulator.get(url,params = params)

  json_response = resp.json()
  assert resp.status_code == 200, "Status should be 200"
  assert json_response["data"]["progress"] == 0, "Progress should be 0"
  assert json_response["data"]["status"] == "not_attempted",(
    "Status should be not_attempted")

def test_get_learner_progress_invalid_learner(clean_firestore):
  learning_resource_dict = deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  url = f"{api_url}/test_learner_id/progress"
  params = {"node_id": learning_resource.id,"node_type": "learning_resources"}
  resp = client_with_emulator.get(url,params = params)

  json_response = resp.json()
  assert resp.status_code == 404, "Status should be 404"
  assert json_response["success"] is False
  assert (json_response["message"]==
  "Learner with uuid test_learner_id not found")

def test_get_learner_progress_invalid_learner_profile(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learning_resource_dict = deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  url = f"{api_url}/{learner.uuid}/progress"
  params = {"node_id": learning_resource.id,"node_type": "learning_resources"}
  resp = client_with_emulator.get(url,params = params)

  json_response = resp.json()
  assert resp.status_code == 404, "Status should be 404"
  assert json_response["success"] is False
  assert (json_response["message"]==
  f"LearnerProfile with learner id {learner.id} not found")

def test_get_learner_progress_invalid_node_type(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}

  if "Teamwork" not in learner_profile_dict["learning_goals"]:
    learner_profile_dict["learning_goals"].append("Teamwork")

  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.learner_id = learner.id
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  learning_resource_dict = deepcopy(BASIC_LEARNING_RESOURCE_EXAMPLE)
  learning_resource = LearningResource.from_dict(learning_resource_dict)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  learning_resource_dict["uuid"] = learning_resource.id

  url = f"{api_url}/{learner.uuid}/progress"
  params = {"node_id": learning_resource.id,"node_type": "learning_resource"}
  resp = client_with_emulator.get(url,params = params)

  json_response = resp.json()
  assert resp.status_code == 422, "Status should be 422"
  assert json_response["success"] is False
  assert json_response["message"]=="Validation Failed"

def test_get_learner_progress_invalid_node_id(clean_firestore):
  learner_dict = BASIC_LEARNER_EXAMPLE
  learner = Learner.from_dict(learner_dict)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_profile_dict = {**BASIC_LEARNER_PROFILE_EXAMPLE}

  if "Teamwork" not in learner_profile_dict["learning_goals"]:
    learner_profile_dict["learning_goals"].append("Teamwork")

  learner_profile = LearnerProfile.from_dict(learner_profile_dict)
  learner_profile.uuid = ""
  learner_profile.learner_id = learner.id
  learner_profile.save()
  learner_profile.uuid = learner_profile.id
  learner_profile.update()

  url = f"{api_url}/{learner.uuid}/progress"
  params = {"node_id": "learning_resource.id","node_type": "learning_resources"}
  resp = client_with_emulator.get(url,params = params)

  json_response = resp.json()
  assert resp.status_code == 404, "Status should be 404"
  assert json_response["success"] is False
  assert (json_response["message"]==
  "Learning Resource with uuid learning_resource.id not found")
