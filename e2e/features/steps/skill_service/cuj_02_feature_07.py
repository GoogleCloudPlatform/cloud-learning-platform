"""
Compare similar skills
"""

import behave
import uuid
from setup import post_method
from test_config import API_URL_SKILL_SERVICE

@behave.given("That a user has the ability to compare skills via Skill Management")
def step_1_1(context):
  context.req_id = "1e70f10b-eea3-456b-9e92-0ece5f8f0705"
  context.req_body = {
    "ids": [context.req_id],
    "input_type": "skill",
    "top_k": 5,
    "output_alignment_sources": {
      "skill_sources": [
        "e2e_osn"
      ],
      "learning_resource_ids": []
    }
  }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to compare similar skills is applied within the management interface with correct request payload")
def step_1_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will retrieve the relevant skills that are similar and serve that data back to the management interface")
def step_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"][context.req_id]["aligned_skills"]["e2e_osn"]) == 5


@behave.given("That a user can compare skills via Skill Management")
def step_2_1(context):
  _id = uuid.uuid4()
  context.req_body = {
    "ids": [str(_id)],
    "input_type": "skill",
    "top_k": 5,
    "output_alignment_sources": {
      "skill_sources": [
        "e2e_osn"
      ],
      "learning_resource_ids": []
    }
  }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to compare similar skills is applied within the management interface with incorrect request payload")
def step_2_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw error to the user")
def step_2_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


@behave.given("That a user is able to compare skills via Skill Management")
def step_3_1(context):
  context.req_body = {
    "ids": [],
    "input_type": "skill",
    "top_k": 5,
    "output_alignment_sources": {
      "skill_sources": [
        "e2e_osn"
      ],
      "learning_resource_ids": []
    }
  }
  context.url = f"{API_URL_SKILL_SERVICE}/unified-alignment/id"


@behave.when("The mechanism to compare similar skills is applied within the management interface with no IDs in request payload")
def step_3_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw validation error to the user")
def step_3_3(context):
  assert context.res.status_code == 422


@behave.given("That a user is able to compute semantic similarity between skills via Skill Management")
def step_3_1(context):
  context.req_body = {
      "id_1": "1c17caad-5580-4d10-85ce-32dc369c5cd7",
      "id_2": "1e70f10b-eea3-456b-9e92-0ece5f8f0705",
      "data_source": "e2e_osn"
      }
  context.url = "http://localhost:9012/skill-service/api/v1/skill/similarity"


@behave.when("The mechanism to compute semantic similarity score is applied within the management interface with valid skill IDs in request payload")
def step_3_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will return a semantic similarity score between the two given skill objects")
def step_3_3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data.get("success") is True, "Success not true"
  assert type(context.res_data.get("data").get("similarity_score")) == float


@behave.given("That a user can compute semantic similarity between skills via Skill Management")
def step_3_1(context):
  context.req_body = {
      "id_1": "1c17caad-5580-4d10-85ce-32dc369c5cd7",
      "id_2": "1e70f10b-eea3",
      "data_source": "e2e_osn"
      }
  context.url = "http://localhost:9012/skill-service/api/v1/skill/similarity"


@behave.when("The mechanism to compute semantic similarity score is applied within the management interface with invalid skill IDs in request payload")
def step_3_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()

@behave.then("Skill Service will throw internal error to the user")
def step_3_3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Invalid Skill ID: 1e70f10b-eea3"


@behave.given("That a user has the ability to compute semantic similarity between skills via Skill Management")
def step_3_1(context):
  context.req_body = {
      "id_1": "1c17caad-5580-4d10-85ce-32dc369c5cd7",
      "data_source": "e2e_osn"
      }
  context.url = "http://localhost:9012/skill-service/api/v1/skill/similarity"


@behave.when("The mechanism to compute semantic similarity score is applied within the management interface with only 1 skill ID in request payload")
def step_3_2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Skill Service will throw validation error to the user as only 1 skill provided")
def step_3_3(context):
  assert context.res.status_code == 422, "Status is not 422"
