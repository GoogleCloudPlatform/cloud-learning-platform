"""test file for learner achievements.py"""
import os
from copy import deepcopy
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.learner_achievements import router
from testing.test_config import (API_URL, TESTING_FOLDER_PATH)
from schemas.schema_examples import (BASIC_LEARNER_EXAMPLE,
                                    BASIC_LEARNER_PROFILE_EXAMPLE,
                                    BASIC_ACHIEVEMENT_EXAMPLE,
                                    BASIC_CURRICULUM_PATHWAY_EXAMPLE)
from common.models import (Learner,LearnerProfile,CurriculumPathway,
Achievement)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from common.utils.http_exceptions import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)
app.include_router(router, prefix="/learner-profile-service/api/v1")
client_with_emulator = TestClient(app)

# assigning url
api_url = f"{API_URL}/learner"

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_learner_achievements_postive(clean_firestore):
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

  achievement_dict = {**BASIC_ACHIEVEMENT_EXAMPLE}
  achievement = Achievement.from_dict(achievement_dict)
  achievement.uuid = ""
  achievement.save()
  achievement.uuid = achievement.id
  achievement.update()
  achievement_uuid = achievement.id

  curriculum_pathway_dict = deepcopy(BASIC_CURRICULUM_PATHWAY_EXAMPLE)
  curriculum_pathway_dict["name"] = "Kubernetes Container Orchestration"
  curriculum_pathway_dict["achievements"].append(achievement_uuid)
  curriculum_pathway = CurriculumPathway.from_dict(curriculum_pathway_dict)
  curriculum_pathway.uuid = ""
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  program_pathway_id = curriculum_pathway.id

  url = f"{api_url}/{learner.uuid}/achievements"
  params = {"program_pathway_id": program_pathway_id}
  resp = client_with_emulator.get(url,params = params)
  assert resp.status_code == 200, "Status should be 200"
  assert resp.json().get("data")[0].get(
      "status") == "not completed","Incorrect status"
